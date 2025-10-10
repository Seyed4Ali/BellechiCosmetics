# backend/models/product.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from uuid import uuid4, UUID
from datetime import datetime
from .category import Category
from .brand import Brand
from .product_gallery import ProductGallery
from .tag import Tag


class Product(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str
    english_name: Optional[str] = None
    description: Optional[str] = None
    price: float
    price_before_discount: Optional[float] = None
    discount_percent: Optional[int] = None
    stock: int = 0
    volume: Optional[str] = None
    rating: Optional[float] = 0
    category_id: Optional[UUID] = Field(default=None, foreign_key="category.id")
    brand_id: Optional[UUID] = Field(default=None, foreign_key="brand.id")
    is_verified: bool = False
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    category: Optional[Category] = Relationship(back_populates="products")
    brand: Optional[Brand] = Relationship(back_populates="products")
    galleries: List["ProductGallery"] = Relationship(back_populates="product")
    tags: List["Tag"] = Relationship(back_populates="products", link_model="ProductTag")
