# backend/create_db.py
from backend.models.base import create_db_and_tables

if __name__ == "__main__":
    create_db_and_tables()
    print("✅ All tables created (SQLModel.metadata.create_all executed).")
