from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, Dict
from ..auth.auth_utils import get_current_user
import json
import aioredis
from sqlalchemy.orm import Session
from .. import models
from . import chat_schemas
from ..database import db_dependancy
from typing import List, Dict, Set

router = APIRouter(prefix="/chat", tags=["Chat"])

REDIS_URL = "redis://localhost"
CHANNEL_NAME = "chat_channel"

@router.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket:WebSocket, room_id:int, current_user:dict=Depends(get_current_user)):
    await websocket.accept()

    redis = await aioredis.from_url(REDIS_URL)
    pubsub= redis.pubsub()
    await pubsub.subscribe(f"{CHANNEL_NAME}:{room_id}")

    try:
        while True:
            data = await websocket.receive_text()

            message_data = {
                'user': current_user['email'],
                'message': data
            }
            await redis.publish(f"{CHANNEL_NAME}:{room_id}", json.dump(message_data))

            msg=await pubsub.get_message(ignore_subscribe_messages=True)
            if msg:
                await websocket.send_text(msg['data'].decode('utf-8'))
    except:
        await pubsub.unsubscribe(f"{CHANNEL_NAME}:{room_id}")
        await redis.close()

def get_user_obj(db:Session, current_user:dict) -> models.User:
    user = db.query(models.User).filter(models.User.email == current_user['email']).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_or_create_direct_room(db:Session, user1_id:int, user2_id:int) -> models.ChatRoom:
    subq=db.query(models.ChatRoomParticipant.room_id).filter(models.ChatRoomParticipant.user_id.in_([user1_id, user2_id])).subquery()
    candidate_rooms = db.query(models.ChatRoom).filter(models.ChatRoom.id.in_(subq)).all()

    for room in candidate_rooms:
        part_ids = {p.user_id for p in room.participants}
        if part_ids == {user1_id, user2_id}:
            return room
        
    room = models.ChatRoom()
    db.add(room)
    db.flush()
    db.add_all([
        models.ChatRoomParticipant(user_id=user1_id, room_id=room.id),
        models.ChatRoomParticipant(user_id=user2_id, room_id=room.id),
    ])
    db.commit()
    db.refresh(room)
    return room


@router.post("/rooms", response_model=chat_schemas.RoomOut)
def create_or_get_room(payload:chat_schemas.RoomCreate, db:db_dependancy, current_user:dict=Depends(get_current_user)):
    me=get_user_obj(db, current_user)
    if payload.peer_user_id == me.id:
        raise HTTPException(status_code=404, detail="Cannot create a chat roomm with yourself")

    peer=db.query(models.User).filter(models.User.id == payload.peer_user_id).first()
    if not peer:
        raise HTTPException(status_code=404, detail="Peer user not found")

    room=get_or_create_direct_room(db, me.id, peer.id)
    return chat_schemas.RoomOut(id=room.id,name=room.name, participant_ids=[p.user_id for p in room.participants])

@router.get("/rooms", response_model=List[chat_schemas.RoomOut])
def list_my_rooms(db:db_dependancy, current_user:dict=Depends(get_current_user)):
    me=get_user_obj(db, current_user)
    parts=db.query(models.ChatRoomParticipant).filter(models.ChatRoomParticipant.user_id== me.id).all()
    
    rooms = [p.room for p in parts]
    out=[]
    for r in rooms:
        out.append(chat_schemas.RoomOut(id=r.id, name=r.name, participant_ids=[p.user_id for p in r.participants]))

    return out

@router.get("/rooms/{room_id}/messages", response_model=List[chat_schemas.MessageOut])
def get_room_messages(db:db_dependancy, room_id:int, current_user:dict=Depends(get_current_user)):
    me=get_user_obj(db, current_user)
    member = db.query(models.ChatRoomParticipant).filter_by(room_id=room_id, user_id=me.id).first()
    if not member:
        raise HTTPException(status_code=403, detail="Not a participant of this room")
    msgs=(db.query(models.Message)
            .filter(models.Message.room_id == room_id)
            .order_by(models.Message.timestamp.asc())
            .all()
            )
    return msgs

@router.post("/rooms/{room_id}/messages", response_model=chat_schemas.MessageOut)
def send_message(room_id:int, payload:chat_schemas.MessageCreate, db:db_dependancy, current_user:dict=Depends(get_current_user)):
    me=get_user_obj(db, current_user)
    member = db.query(models.ChatRoomParticipant).filter_by(room_id=room_id, user_id=me.id).first()
    if not member:
        raise HTTPException(status_code=403, detail="Not a participant in this room")

    msg = models.Message(sender_id=me.id, room_id=room_id, content=payload.content)
    db.add(msg)
    db.commit()
    db.refresh(msg)

    awaitable = ConnectionManager.broadcast({
        'type':'message',
        'room_id':room_id,
        'sender_id':me.id,
        'content':payload.content,
        'message_id':msg.id,
        'timestamp': msg.timestamp.isoformat()
    })

    try:
        import asyncio
        if asyncio.get_running_loop().is_running():
            asyncio.create_task(awaitable)
    except RuntimeError:
        pass

    return msg

class ConnectionManager:
    rooms:Dict[int, Set[WebSocket]] = {}

    @classmethod
    async def connect(cls, room_id:int, websocket:WebSocket):
        await websocket.accept()
        cls.rooms.setdefault(room_id, set()).add(websocket)
    
    @classmethod
    def disconnect(cls, room_id:int, websocket:WebSocket):
        for room_id in cls.rooms and websocket in cls.rooms[room_id]:
            cls.rooms[room_id].remove(websocket)
            if not cls.rooms[room_id]:
                del cls.rooms[room_id]
    
    @classmethod
    async def broadcast(cls, room_id:int, payload:dict):
        import json
        message = json.dumps(payload)
        for ws in list(cls.rooms.get(room_id, [])):
            try:
                await ws.send_text(message)
            except:
                cls.disconnect(room_id, ws)
   