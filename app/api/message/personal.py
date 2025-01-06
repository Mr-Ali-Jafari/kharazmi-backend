from typing import Dict
from fastapi import WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from app.models.models import PersonalMessage as model
from app.models.models import ChatUser
from fastapi import APIRouter
from app.config.database.database import get_db
from app.schemas.schemas import Message
from typing import List
router = APIRouter(
    prefix='/personal'
)

class PersonalMessageManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.active_connections[username] = websocket
        print(f"{username} connected.")

    def disconnect(self, websocket: WebSocket, username: str):
        if username in self.active_connections:
            del self.active_connections[username]
            print(f"{username} disconnected.")
    
    async def send_personal_message(self, message: str, sender: str, receiver: str, db: Session):
        # ذخیره پیام در پایگاه داده
        db_message = model(sender=sender, receiver=receiver, content=message)
        db.add(db_message)
        db.commit()



        # ارسال پیام اگر کاربر مقصد متصل است
        websocket = self.active_connections.get(receiver)
        if websocket:
            await websocket.send_text(message)
        else:
            print(f"User {receiver} is not connected.")

personal_message_manager = PersonalMessageManager()

@router.websocket("/ws/{username}/{sender}")
async def websocket_endpoint_personal(websocket: WebSocket, username: str, sender: str, db: Session = Depends(get_db)):
    await personal_message_manager.connect(websocket, username=username)
    
    try:
        while True:
            data = await websocket.receive_text()

            await personal_message_manager.send_personal_message(message=data, sender=sender, receiver=username, db=db)

    except WebSocketDisconnect:
        personal_message_manager.disconnect(websocket, username=username)




@router.get("/messages/{username1}/{username2}", response_model=List[Message])
def get_messages(username1: str, username2: str, db: Session = Depends(get_db)):
    messages = db.query(model).filter(
        (model.sender == username1) & (model.receiver == username2) |
        (model.sender == username2) & (model.receiver == username1)
    ).all()

    return messages