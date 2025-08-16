from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class RoomCreate(BaseModel):
    peer_user_id:int

class RoomOut(BaseModel):
    id: int
    name:Optional[str] = None
    participant_ids: List[int]

    class Config:
        from_attributes=True

class MessageCreate(BaseModel):
    content: str

class MessageOut(BaseModel):
    id:int
    sender_id:int
    room_id:int
    content:str
    timestamp:datetime

    class Config:
        from_attributes=True