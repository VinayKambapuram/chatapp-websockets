# FastAPI WebSocket Chat Application
A real-time chat application built with FastAPI and WebSockets, allowing multiple users to join and exchange messages instantly.

## Features
✅ Real-time messaging with WebSockets      
✅ Supports multiple users in a chat room  
✅ Serves static files (JS & CSS) and HTML templates  
✅ Managed with Pipenv for easy dependency handling

## Installation
### 1️⃣ Clone the Repository
https://github.com/VinayKambapuram/chatapp-websockets.git
cd chatapp

### 2️⃣ Install Dependencies
pipenv install  

### 3️⃣ Activate Virtual Environment
pipenv shell  

### 4️⃣ Run the Server  
uvicorn main:app --reload

### 5️⃣ Open in Browser  
http://127.0.0.1:8000/

## Project Structure

/chatapp  
│── /static                 # Static files  
│   ├── /js                  # JavaScript & CSS  
│   │   ├── script.js         # WebSocket logic  
│   │   ├── styles.css      # Chat UI styling  
│── /templates              # HTML templates  
│   ├── index.html          # Chat interface  
│── main.py                 # FastAPI application  
│── Pipfile                 # Pipenv dependencies  
│── Pipfile.lock            # Pipenv lock file  
│── README.md               # Project documentation  

## WebSocket Endpoint
📡 WebSocket URL: ws://localhost:8000/message

Users connect via WebSockets.  
Messages are broadcast to all connected users.  
Handles user disconnections automatically.  
