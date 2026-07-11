import json
from typing import Optional
from pathlib import Path
from pydantic import BaseModel
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi import Request
from collections import deque
from fastapi.templating import Jinja2Templates
from pathlib import Path
from fastapi.staticfiles import StaticFiles

HISTORY_FILE = Path("data/messages.json")
HISTORY_FILE.parent.mkdir(exist_ok=True)

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "app.db"

app = FastAPI()



connections = set()

templates = Jinja2Templates(directory="app/frontend/templates")

app.mount("/static", StaticFiles(directory="app/frontend/static"), name="static")

def load_messages():
    if not HISTORY_FILE.exists():
        return []

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()

            if not content:   # 🔥 пустой файл
                return []

            return json.loads(content)

    except Exception:
        return []


def save_messages(messages):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(list(messages), f, ensure_ascii=False, indent=2)


messages = deque(load_messages(), maxlen=100)

class IngestRequest(BaseModel):
    text: str
    source: Optional[str] = "unknown"

async def broadcast(message: dict):
    dead = []

    for ws in connections:
        try:
            await ws.send_json(message)
        except:
            dead.append(ws)

    for ws in dead:
        connections.remove(ws)


@app.post("/ingest")
async def ingest(data: IngestRequest):
    msg = {
        "text": data.text,
        "source": data.source
    }
    messages.append(msg)
    save_messages(messages)
    await broadcast(msg)
    print(f"[{data.source}] {data.text}")
    return {"status": "ok"}

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    connections.add(ws)

    try:
        # отправляем историю при подключении
        for msg in messages:
            await ws.send_json(msg)

        while True:
            await ws.receive_text()  # держим соединение живым

    except WebSocketDisconnect:
        connections.remove(ws)


@app.get("/ingest")
def get_messages():
    return list(messages)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})