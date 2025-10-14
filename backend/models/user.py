# backend/models/user.py
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, date
from pydantic import validator, EmailStr, root_validator
import re
from uuid import UUID, uuid4
from .address import Address
from .cart import CartItem
from .wallet import Wallet
from .order import Order
from .comment import Commemt


class User(SQLModel, table=True):
   
    # کلید اصلی دیتابیس، خودکار و یکتا
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    # اطلاعات ورود، حداقل یکی باید موجود باشد
    email: Optional[str] = Field(default=None, index=True, unique=True, nullable=True)
    phone: Optional[str] = Field(default=None, index=True,  unique=True, nullable=True)

    # OAuth (فعلاً فقط گوگل)
    oauth_provider: Optional[str] = Field(default=None, max_length=20)  # "google"
    oauth_id: Optional[str] = None  # شناسه کاربر گوگل

    # اطلاعات شخصی
    first_name: str = Field(..., max_length=40)
    last_name: str = Field(..., max_length=40)
    birth_date: Optional[date] = None
    is_birth_date_set: bool = False  # برای محدودیت یکبار پر کردن

    # وضعیت‌ها
    is_active: bool = True
    is_email_verified: bool = False
    is_phone_verified: bool = False

    # زمان‌ها
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # ارتباط‌ها
    addresses: list["Address"] = Relationship(back_populates="user")
    cart: Optional["Cart"] = Relationship(back_populates="user", sa_relationship_kwargs={"uselist": False})
    wallet: Optional["Wallet"] = Relationship(back_populates="user", sa_relationship_kwargs={"uselist": False})
    orders: List["Order"] = Relationship(back_populates="user")
    comments: List["Comment"] = Relationship(back_populates="user")

    # ولیدیشن شماره تلفن
    @validator("phone")
    def phone_must_be_11_digits(cls, v):
        if v is None:
            return v
        digits = re.sub(r"\D", "", v)
        if len(digits) != 11:
            raise ValueError(".شماره باید 11 رقم باشد")
        return digits

    # ولیدیشن ایمیل
    @validator("email")
    def email_must_be_valid(cls, v):
        if v is None:
            return v
        try:
            EmailStr.validate(v)
        except Exception:
            raise ValueError("ایمیل معتبر نیست")
        return v.lower()

    # چک کردن اینکه حداقل یکی از phone یا email موجود باشد
    @root_validator
    def at_least_one_contact(cls, values):
        phone, email = values.get('phone'), values.get('email')
        if not phone and not email:
            raise ValueError("ایمیل یا شماره تلفن باید وارد شود")
        return values

# جدول OTP برای ارسال کد یکبار مصرف
class OTP(SQLModel, table=True):

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: Optional[UUID] = Field(default=None, foreign_key="users.id")  # ارتباط با User
    code: str = Field(max_length=6)  # کد OTP ۶ رقمی
    method: str = Field(max_length=10)  # "sms" یا "email"
    is_used: bool = False
    expires_at: datetime = Field(default_factory=lambda: datetime.utcnow() + timedelta(minutes=5))
    created_at: datetime = Field(default_factory=datetime.utcnow)