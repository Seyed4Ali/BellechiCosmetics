from uuid import UUID, uuid4
from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from .product import Product
from .blog import Blog

class ProductTagLink(SQLModel, table=True):
    product_id: UUID = Field(foreign_key="product.id", primary_key=True)
    tag_id: UUID = Field(foreign_key="tag.id", primary_key=True)

class BlogTagLink(SQLModel, table=True):
    blog_id: UUID = Field(foreign_key="blog.id", primary_key=True)
    tag_id: UUID = Field(foreign_key="tag.id", primary_key=True)

class Tag(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True, unique=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Backrefs: از نوع استرینگ نوشتیم تا circular import پیش نیاد
    products: List["Product"] = Relationship(back_populates="tags", link_model=ProductTagLink)
    blogs: List["Blog"] = Relationship(back_populates="tags", link_model=BlogTagLink)