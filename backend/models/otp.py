# backend/models/otp.py
from sqlmodel import SQLModel, Field, Relationship
from uuid import uuid4, UUID
from typing import Optional, List
from datetime import datetime

class OTP(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    user_id: Optional[UUID] = Field(default=None, foreign_key="user.id")
    code: str
    purpose: str
    expires_at: Optional[datetime]
    used: bool = False
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
