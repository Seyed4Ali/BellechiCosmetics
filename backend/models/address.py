# backend/models/address.py
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from uuid import UUID, uuid4
from .user import User

class Address(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id")
    country: Optional[str] = None
    city: Optional[str] = None
    street: Optional[str] = None
    postal_code: Optional[str] = None
    is_default: bool = False
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    user: "User" = Relationship(back_populates="addresses")
