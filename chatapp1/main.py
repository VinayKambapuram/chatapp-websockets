from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from faker import Faker


app = FastAPI()
fake = Faker()


@app.get("/", response_class=HTMLResponse)
async def homepage():
    
    # Serves a simple HTML page with a WebSocket connection.
    
    return """
    <html>
        <head>
            <title>Chat</title>
        </head>
        <body>
            <h2>Websocket Chat App</h2>
            <input id="messageInput" type="text">
            <button onclick="sendMessage()">Send</button>
            <ul id="messages"></ul>
            <script>
                let ws = new WebSocket("ws://localhost:8000/ws");
                ws.onmessage = event => {
                    let li = document.createElement('li');
                    li.textContent = event.data;
                    document.getElementById("messages").appendChild(li);
                };
                function sendMessage() {
                    let input = document.getElementById("messageInput");
                        ws.send(input.value);
                        input.value = "";
                    } 
            </script>
        </body>
    </html>

    """

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint that listens for incoming messages and responds.
    """
    # accepts WebSocket connection
    await websocket.accept()
    while True:
        # Receives message from client
        data = await websocket.receive_text()

        # Checks if the user wants fake data
        if data.lower() == "user":
            response = {"username" :fake.user_name(),
                        "email": fake.email(),
                        "address": fake.address()
                        }
        else:
            response = {"message": fake.sentence()}

        # Sends the response back to the client
        await websocket.send_json(response)
        



