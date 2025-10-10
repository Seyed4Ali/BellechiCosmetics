# backend/models/user.py
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, date
from pydantic import validator, EmailStr
import re
from uuid import UUID, uuid4
from address import Address

class User(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: Optional[str] = Field(default=None, index=True, unique=True)
    phone: Optional[str] = Field(default=None, index=True)
    hashed_password: Optional[str] = None
    full_name: str
    last_name: str
    birth_date: Optional[date] = None
    is_birth_date_set: bool = False
    is_active: bool = True
    is_email_verified: bool = False
    is_phone_verified: bool = False
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    addresses: list["Address"] = Relationship(back_populates="user")

    @validator("phone")
    def phone_must_be_11_digits(cls, v):
        if v is None:
            return v
        digits = re.sub(r"\D", "", v)
        if len(digits) != 11:
            raise ValueError("phone must contain exactly 11 digits")
        return digits

    @validator("email")
    def email_must_be_gmail(cls, v):
        if v is None:
            return v
        # use simple check (domain)
        if not v.lower().endswith("@gmail.com"):
            raise ValueError("email must be a gmail address (end with @gmail.com)")
        return v

    # helper: generate username if not provided
    @staticmethod
    def generate_username_from(phone: Optional[str], email: Optional[str]) -> str:
        if phone:
            return phone
        if email:
            return email.split("@")[0]
        # fallback
        return f"user_{uuid4().hex[:8]}"
