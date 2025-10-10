# backend/models/payment.py
from sqlmodel import SQLModel, Field, Relationship
from uuid import uuid4, UUID
from typing import Optional, List
from datetime import datetime

class Payment(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    order_id: UUID = Field(foreign_key="order.id")
    payment_method: str
    amount: float
    status: str = "pending"
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
