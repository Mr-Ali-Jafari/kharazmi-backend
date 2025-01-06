from typing import List
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Depends
from datetime import datetime
from app.config.database.database import get_db
from sqlalchemy.orm import Session
from app.models.models import Message,PersonalMessage,Group

from app.schemas.schemas import GroupCreateRequest
router = APIRouter(
    prefix="/chat",
    tags=["message"]
)


from fastapi import WebSocket
from typing import List, Dict

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.group_members: dict = {}
        self.user_connections: Dict[str, WebSocket] = {} 

    async def connect(self, websocket: WebSocket, group_name: str, username: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.user_connections[username] = websocket 
        
        if group_name not in self.group_members:
            self.group_members[group_name] = []
        self.group_members[group_name].append(websocket)

    def disconnect(self, websocket: WebSocket, group_name: str, username: str):
        self.active_connections.remove(websocket)
        if group_name in self.group_members:
            self.group_members[group_name].remove(websocket)
        
        if username in self.user_connections:
            del self.user_connections[username]

    async def send_personal_message(self, message: str, username: str):
        websocket = self.user_connections.get(username) 
        if websocket:
            await websocket.send_text(message)
        else:
            print(f"User {username} is not connected.")

    async def broadcast(self, message: str, group_name: str):
        if group_name in self.group_members:
            for connection in self.group_members[group_name]:
                await connection.send_text(message)




connection_manager = ConnectionManager()

@router.post("/create-group")
def create_group(data: GroupCreateRequest, db: Session = Depends(get_db)):
    existing_group = db.query(Group).filter(Group.name == data.name).first()
    if existing_group:
        raise HTTPException(status_code=400, detail="Group with this name already exists")
    
    new_group = Group(name=data.name, description=data.description)
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    
    return {
        "message": "Group created successfully",
        "group": {
            "name": new_group.name,
            "description": new_group.description
        }
    }


@router.websocket("/ws/{group_name}/{client_name}")
async def websocket_endpoint(websocket: WebSocket, group_name: str, client_name: str, db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.name == group_name).first()
    if not group:
        await websocket.close()
        raise HTTPException(status_code=404, detail="Group not found")

    await connection_manager.connect(websocket, group_name)
    try:
        while True:
            data = await websocket.receive_text()
            new_message = Message(text=data, sender=client_name, group_id=group.id)
            db.add(new_message)
            db.commit()
            await connection_manager.broadcast(f"{client_name}: {data}", group_name)
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket, group_name)
        await connection_manager.broadcast(f"Client #{client_name} left the chat", group_name)







@router.get("/messages/{group_name}")
def get_messages(group_name: str, db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.name == group_name).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    messages = db.query(Message).filter(Message.group_id == group.id).order_by(Message.timestamp).all()
    return {"group": group_name, "messages": [{"sender": msg.sender, "text": msg.text, "timestamp": msg.timestamp} for msg in messages]}


@router.get("/groups")
def get_groups(db: Session = Depends(get_db)):
    """
    Retrieve all available groups from the database.
    """
    groups = db.query(Group).all()
    if not groups:
        raise HTTPException(status_code=404, detail="No groups found")
    return {"groups": [{"id": group.id, "name": group.name, "description": group.description} for group in groups]}