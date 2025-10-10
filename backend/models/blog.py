from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime
from .user import User
from .tag import Tag

class BlogTagLink(SQLModel, table=True):
    blog_id: UUID = Field(foreign_key="blog.id", primary_key=True)
    tag_id: UUID = Field(foreign_key="tag.id", primary_key=True)


class Blog(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(index=True)
    slug: str = Field(index=True, unique=True)
    summary: Optional[str] = Field(default=None)
    content: str
    author_id: UUID = Field(foreign_key="user.id")
    published_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # روابط
    author: Optional["User"] = Relationship(back_populates="blogs")
    tags: List["Tag"] = Relationship(back_populates="blogs", link_model=BlogTagLink)
