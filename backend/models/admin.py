# backend/models/admin.py
from sqlmodel import SQLModel, Field, Relationship
from uuid import uuid4, UUID
from typing import Optional, List
from datetime import datetime
from .blog import Blog

class Admin(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    first_name: str
    last_name: str
    username: str = Field(index=True, unique=True)
    hashed_master_code: str 
    role: str  
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    blogs: List["Blog"] = Relationship(back_populates="author")
