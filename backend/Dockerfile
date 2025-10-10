# از ایمیج رسمی پایتون استفاده می‌کنیم
FROM python:3.11-slim

# تنظیم دایرکتوری کاری داخل کانتینر
WORKDIR /app

# فایل‌های requirements رو کپی و نصب کن
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# بقیه کدهای backend رو کپی کن
COPY . .

# پورت FastAPI
EXPOSE 8000

# فرمان اجرای برنامه
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
