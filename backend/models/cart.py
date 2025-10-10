# backend/models/cart.py
from sqlmodel import SQLModel, Field, Relationship
from uuid import uuid4, UUID
from typing import Optional, List
from datetime import datetime

class CartItem(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", index=True)
    product_id: UUID = Field(foreign_key="product.id")
    quantity: int = 1
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)