from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


template = Jinja2Templates(directory="chatapp2/templates")

app = FastAPI()
app.mount("/static", StaticFiles(directory="chatapp2\static"), name="static")


@app.get("/")
async def get(request: Request):
    return template.TemplateResponse("index.html", {"request" : request, "title": "Chat App2"})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")