# backend/models/__init__.py
from .base import engine, SQLModel, create_db_and_tables
from .user import User, UserCreate, UserRead
from .address import Address, AdressCreate, AddressRead
from .admin import Admin,  AdminCreate, AdminRead
from .blog import Blog, BlogTagLink, BlogCreate, BlogRead
from .brand import Brand, BrandCreate, BrandRead
from .cart import CartItem, CartCreate, CartRead
from .category import Category, CategoryCreate, CategoryRead
from .order_item import OrderItem
from .order import Order, OrderCreate, OrderRead
from .otp import OTP, OTPCreate, OTPRead
from .payment import Payment, PaymentCreate, PaymentRead
from .product import Product, ProductCreate, ProductRead
from .product_gallery import ProductGallery, ProductGalleryCreate, ProductGalleryRead
from .tag import Tag, TagCreate, TagRead

# import other models as needed

__all__ = ["engine", "SQLModel", "create_db_and_tables", "User", "Address", "Admin", ""]
