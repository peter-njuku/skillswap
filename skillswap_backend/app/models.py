from sqlalchemy import Column, String, Integer, ForeignKey, Text, DateTime, Boolean, func
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    skills_teach = Column(Text, nullable=True)
    skills_learn = Column(Text, nullable=True)

    skills = relationship("Skill", back_populates="owner")
    chat_participants = relationship("ChatRoomParticipant", back_populates="user")
    sent_messages = relationship("Message", back_populates="sender")
    notifications = relationship("Notification",back_populates="user")

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    owner = relationship("User", back_populates="skills")

class ChatRoom(Base):
    __tablename__ ="chat_rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime,default=datetime.utcnow())

    messages = relationship("Message", back_populates="room", cascade="all, delete")
    participants = relationship("ChatRoomParticipant", back_populates="room", cascade="all, delete")

class ChatRoomParticipant(Base):
    __tablename__ = "chat_participants"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    room_id = Column(Integer, ForeignKey("chat_rooms.id"))

    room=relationship("ChatRoom", back_populates="participants")
    user=relationship("User", back_populates="chat_participants")

class Message(Base):
    __tablename__= "messages"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    room_id = Column(Integer, ForeignKey("chat_rooms.id"))
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    room=relationship("ChatRoom", back_populates="messages")
    sender=relationship("User", back_populates="sent_messages")

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id=Column(Integer, ForeignKey("users.id"))
    type=Column(String)
    content=Column(String)
    is_read=Column(Boolean, default=False)
    created_at=Column(DateTime, server_default=func.now())
    
    user=relationship("User", back_populates="notifications")