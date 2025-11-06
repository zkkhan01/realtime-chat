from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from typing import List, Set
from sqlmodel import Session, select
from .db import init_db, get_session
from .models import Message

app = FastAPI(title="Realtime Chat")
clients: Set[WebSocket] = set()

@app.on_event("startup")
def startup(): init_db()

@app.get("/messages")
def list_messages(limit: int = 50, session: Session = Depends(get_session)):
    q = select(Message).order_by(Message.created_at.desc()).limit(limit)
    rows = list(reversed(session.exec(q).all()))
    return [{"user":m.user,"text":m.text,"created_at":m.created_at.isoformat()} for m in rows]

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    clients.add(ws)
    try:
        while True:
            data = await ws.receive_json()
            # Expect: {user, text}
            m = Message(user=data.get("user","anon"), text=data.get("text",""))
            from .db import get_session as gs
            for session in gs():
                session.add(m); session.commit()
            # broadcast
            for c in list(clients):
                try:
                    await c.send_json({"user": m.user, "text": m.text})
                except Exception:
                    pass
    except WebSocketDisconnect:
        clients.discard(ws)
