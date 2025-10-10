# backend/models/__init__.py
from .base import engine, SQLModel, create_db_and_tables
from .user import User, UserCreate, UserRead
from .address import Address
# import other models as needed

__all__ = ["engine", "SQLModel", "create_db_and_tables", "User", "Address"]
