from logging.config import fileConfig
from sqlmodel import SQLModel
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys
from dotenv import load_dotenv

# اضافه کردن مسیر backend به sys.path تا import مدل‌ها راحت انجام بشه
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import تمام مدل‌ها تا Alembic بتونه شِمای جداول رو تشخیص بده
from models.user import User
from models.product import Product
from models.category import Category
from models.order import Order, OrderItem
from models.cart import CartItem
from models.address import Address
from models.payment import Payment
from models.blog import Blog
from models.tag import Tag, BlogTagLink, ProductTagLink
from models.brand import Brand

# پیکربندی Alembic
config = context.config

# تنظیمات logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# این بخش خیلی مهمه:
# Alembic باید بدونه از کجا metadata بگیره.
target_metadata = SQLModel.metadata

# دریافت URL دیتابیس از ENV (در docker-compose یا .env)
def get_url():
    load_dotenv()
    DATABASE_URL = os.getenv("DATABASE_URL")


def run_migrations_offline():
    """اجرای مهاجرت در حالت offline"""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """اجرای مهاجرت در حالت online"""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=get_url(),
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
