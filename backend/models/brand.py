# backend/models/brand.py
from sqlmodel import SQLModel, Field, Relationship
from uuid import uuid4, UUID
from typing import Optional, List
from .product import Product

class Brand(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True, unique=True)
    image: Optional[str] = None
    products: List["Product"] = Relationship(back_populates="brand")
