from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    email: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    class Config:
        from_attributes = True

class MessageBase(BaseModel):
    subject: str
    body: str

class MessageCreate(MessageBase):
    recipient_id: int

class Message(MessageBase):
    id: int
    sender_id: int
    recipient_id: int
    timestamp: datetime
    class Config:
        from_attributes = True

class InboxBase(BaseModel):
    user_id: int
    message_id: int
    is_read: bool

class InboxCreate(InboxBase):
    pass

class Inbox(InboxBase):
    id: int
    class Config:
        from_attributes = True
