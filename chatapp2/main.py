import os
from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect
from fastapi.responses import HTMLResponse, RedirectResponse
from dataclasses import dataclass
import uuid
import json
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware



# WebSocket Connection Manager Class

@dataclass
class ConnectionManager():
    """ Manages active WebSocket connections """
    
    def __init__(self):
        # Dictionary to store active WebSocket connections with unique IDs
        self.active_connections: dict = {}

    async def connect(self, websocket: WebSocket):
        """ Accepts a WebSocket connection and assigns a unique ID to the user """
        await websocket.accept()
        user_id = str(uuid.uuid4())  # Generate a unique user ID
        self.active_connections[user_id] = websocket  # Store the connection
        
        # Notify the user that they have joined
        data = json.dumps({"isMe": True, "data": "Have joined the chat", "username": "You"})
        await self.send_message(websocket, data)

    async def send_message(self, ws: WebSocket, message: str):
        """ Sends a message to a specific WebSocket client """
        await ws.send_text(message)

    async def broadcast(self, websocket: WebSocket, data: str):
        """ Broadcasts a message to all connected clients """
        decoded_data = json.loads(data)  # Convert JSON string to Python dictionary

        for connection in self.active_connections.values():
            is_me = connection == websocket  # Check if the sender is the current user

            # Send message to all users with sender identification
            await connection.send_text(json.dumps({
                "isMe": is_me,
                "data": decoded_data['message'],
                "username": decoded_data['username']
            }))

    async def disconnect(self, websocket: WebSocket):
        """ Removes a disconnected WebSocket connection """
        user_id = self.find_id(websocket)  # Find the user ID associated with the WebSocket
        if user_id:
            del self.active_connections[user_id]  # Remove the user from active connections
        return user_id

    def find_id(self, websocket: WebSocket):
        """ Finds the user ID based on the WebSocket object """
        for user_id, ws in self.active_connections.items():
            if ws == websocket:
                return user_id
        return None


# FastAPI Application Setup

# Get the base directory of the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Setup Jinja2 template rendering for HTML responses
template = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Initialize FastAPI application
app = FastAPI()

# Enable CORS (Cross-Origin Resource Sharing) to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (update this to restrict domains)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Serve static files (CSS, JavaScript, etc.)
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# Create an instance of the connection manager
connection_manager = ConnectionManager()



#  Web Routes
@app.get("/", response_class=HTMLResponse)
async def get(request: Request):
    """ Serves the main chat page """
    return template.TemplateResponse("index.html", {"request": request, "title": "Chat App2"})


@app.get("/join", response_class=HTMLResponse)
async def get_room(request: Request):
    """ Serves the chat room selection page """
    return template.TemplateResponse("room.html", {"request": request})


#  WebSocket Endpoint for Chat
@app.websocket("/message")
async def websocket_endpoint(websocket: WebSocket):
    """ Handles WebSocket connections for real-time chat """
    
    await connection_manager.connect(websocket)  # Add user to active connections

    try:
        while True:
            # Receive message from the user
            data = await websocket.receive_text()
            await connection_manager.broadcast(websocket, data)  # Broadcast to all users
    except WebSocketDisconnect:
        # If a user disconnects, remove them from active connections
        user_id = await connection_manager.disconnect(websocket)
        return RedirectResponse(url="/")  # Redirect user to the main page after disconnecting
