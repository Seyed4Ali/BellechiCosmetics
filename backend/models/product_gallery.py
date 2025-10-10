# backend/models/product_gallery.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from uuid import uuid4, UUID
from .product import Product

class ProductGallery(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    product_id: UUID = Field(foreign_key="product.id")
    url: str
    is_video: bool = False
    product: "Product" = Relationship(back_populates="galleries")
