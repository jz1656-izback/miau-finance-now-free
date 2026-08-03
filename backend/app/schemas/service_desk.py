from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TicketCreate(BaseModel):
    category: str = "question"
    priority: str = "medium"
    title: str
    description: Optional[str] = None
    author: Optional[str] = None
    service: Optional[str] = None


class TicketUpdate(BaseModel):
    status: Optional[str] = None
    assigned_to: Optional[str] = None


class TicketPoke(BaseModel):
    pass


class TicketResponse(BaseModel):
    id: str
    category: str
    priority: str
    title: str
    description: Optional[str] = None
    author: Optional[str] = None
    service: Optional[str] = None
    status: str
    assigned_to: Optional[str] = None
    pokes: int = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True
