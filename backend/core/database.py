from sqlmodel import SQLModel, Session, create_engine
from dotenv import load_dotenv
import os

# 1️⃣ بارگذاری فایل .env
load_dotenv()

# 2️⃣ گرفتن URL دیتابیس از ENV یا مقدار پیش‌فرض (برای Docker)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/bellechi")

# 3️⃣ ساخت Engine
engine = create_engine(DATABASE_URL, echo=False)

# 4️⃣ تابع ساخت جدول‌ها (فقط هنگام توسعه)
def init_db():
    """
    فقط در محیط توسعه استفاده میشه تا جدول‌ها در صورت نبود ساخته بشن.
    در محیط production از Alembic برای migration استفاده کن.
    """
    SQLModel.metadata.create_all(engine)

# 5️⃣ تابع ایجاد Session (برای CRUDها)
def get_session():
    with Session(engine) as session:
        yield session
