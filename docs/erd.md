# ERD — BellechiCosmetics (نسخه اولیه)
## کپی کن داخل docs/erd.md. این شامل توضیح خلاصه و DBML برای dbdiagram (می‌تونی در https://dbdiagram.io  پیست کنی و خروجی PNG بگیری).
## توضیح کلی
موجودیت‌ها: User, Address, Wallet, Category, Brand, Product, ProductGallery, Tag, ProductTag (association), CartItem, Order, OrderItem, Payment, Blog, BlogImage, Admin, OTP, SearchHistory, ChatMessage, ProductVerification, Review

- تاریخچه‌های قابل حذف: SearchHistory, ChatMessage, CartItem
- تاریخچهٔ خرید (Order, OrderItem, Payment, Review) غیرقابل حذف (حتماً بماند)
- هر User حداقل یک Address دارد (اول در ثبت‌نام ذخیره می‌شود)
- Adminها از جدول جدا خوانده می‌شوند؛ ورود ادمین با username = last_name و کد 6 رقمی ایمیل‌شده. یک کد 12 رقمی "master_code" فقط در سرور مدیر نگهداری شود (هش شده).

## DBML (برای وارد کردن در dbdiagram.io)
Table users {
  id uuid [pk, default: `gen_random_uuid()`]
  username varchar [unique, not null]       // شناسه اصلی کاربر (ممکنه phone/email/generated)
  email varchar [unique]
  phone varchar
  hashed_password varchar
  full_name varchar [not null]
  last_name varchar [not null]
  birth_date date
  is_birth_date_set boolean [default: false] // برای یک‌بار پر شدن
  is_active boolean [default: true]
  is_email_verified boolean [default: false]
  is_phone_verified boolean [default: false]
  created_at timestamptz [default: `now()`]
  updated_at timestamptz
}

Table addresses {
  id uuid [pk, default: `gen_random_uuid()`]
  user_id uuid [ref: > users.id]
  country varchar
  city varchar
  street text
  postal_code varchar
  is_default boolean [default: false]
  created_at timestamptz [default: `now()`]
}

Table wallets {
  id uuid [pk, default: `gen_random_uuid()`]
  user_id uuid [ref: > users.id]
  balance numeric(12,2) [default: 0]
  created_at timestamptz [default: `now()`]
}

Table categories {
  id uuid [pk, default: `gen_random_uuid()`]
  name varchar [not null, unique]
  image varchar
  created_at timestamptz [default: `now()`]
}

Table brands {
  id uuid [pk, default: `gen_random_uuid()`]
  name varchar [not null, unique]
  image varchar
  created_at timestamptz [default: `now()`]
}

Table products {
  id uuid [pk, default: `gen_random_uuid()`]
  name varchar [not null]
  english_name varchar
  description text
  price numeric(12,2) [not null]
  price_before_discount numeric(12,2)
  discount_percent int
  stock int [default: 0]
  volume varchar
  rating numeric(3,2) [default: 0]
  category_id uuid [ref: > categories.id]
  brand_id uuid [ref: > brands.id]
  is_verified boolean [default: false]
  created_at timestamptz [default: `now()`]
}

Table product_galleries {
  id uuid [pk, default: `gen_random_uuid()`]
  product_id uuid [ref: > products.id]
  url varchar
  is_video boolean [default: false]
}

Table tags {
  id uuid [pk, default: `gen_random_uuid()`]
  name varchar [not null, unique]
}

Table product_tags {
  product_id uuid [ref: > products.id]
  tag_id uuid [ref: > tags.id]
  indexes {
    (product_id, tag_id) [unique]
  }
}

Table cart_items {
  id uuid [pk, default: `gen_random_uuid()`]
  user_id uuid [ref: > users.id]
  product_id uuid [ref: > products.id]
  quantity int [default: 1]
  created_at timestamptz [default: `now()`]
}

Table orders {
  id uuid [pk, default: `gen_random_uuid()`]
  user_id uuid [ref: > users.id]
  address_id uuid [ref: > addresses.id]
  total_amount numeric(12,2)
  status varchar [default: 'pending'] // pending, paid, shipped, delivered, canceled
  created_at timestamptz [default: `now()`]
  updated_at timestamptz
}

Table order_items {
  id uuid [pk, default: `gen_random_uuid()`]
  order_id uuid [ref: > orders.id]
  product_id uuid [ref: > products.id]
  quantity int
  unit_price numeric(12,2)
}

Table payments {
  id uuid [pk, default: `gen_random_uuid()`]
  order_id uuid [ref: > orders.id]
  payment_method varchar
  amount numeric(12,2)
  status varchar [default: 'pending'] // pending, success, failed
  created_at timestamptz [default: `now()`]
}

Table blogs {
  id uuid [pk, default: `gen_random_uuid()`]
  title varchar
  slug varchar [unique]
  summary text
  content text
  author_id uuid [ref: > users.id]
  published_at timestamptz
  created_at timestamptz [default: `now()`]
}

Table blog_images {
  id uuid [pk, default: `gen_random_uuid()`]
  blog_id uuid [ref: > blogs.id]
  url varchar
}

Table admins {
  id uuid [pk, default: `gen_random_uuid()`]
  first_name varchar
  last_name varchar
  username varchar [unique] // پیشنهاد: last_name indexed
  hashed_master_code varchar // هش‌شده کد 12 رقمی (از env یا vault)
  role varchar // owner, manager, assistant, writer
  created_at timestamptz [default: `now()`]
}

Table otps {
  id uuid [pk, default: `gen_random_uuid()`]
  user_id uuid [ref: > users.id]
  code varchar
  purpose varchar // 'login', 'verify_email', 'verify_phone', 'admin_login'
  expires_at timestamptz
  used boolean [default: false]
  created_at timestamptz [default: `now()`]
}

Table search_histories {
  id uuid [pk, default: `gen_random_uuid()`]
  user_id uuid [ref: > users.id]
  query text
  created_at timestamptz [default: `now()`]
}

Table chat_messages {
  id uuid [pk, default: `gen_random_uuid()`]
  user_id uuid [ref: > users.id]
  agent varchar // user / support / ai
  content text
  created_at timestamptz [default: `now()`]
}

Table product_verifications {
  id uuid [pk, default: `gen_random_uuid()`]
  product_id uuid [ref: > products.id]
  report_text text
  report_image varchar
  reporter_user_id uuid [ref: > users.id]
  status varchar [default: 'pending'] // pending, confirmed_fake, confirmed_real
  created_at timestamptz [default: `now()`]
}

Table reviews {
  id uuid [pk, default: `gen_random_uuid()`]
  product_id uuid [ref: > products.id]
  user_id uuid [ref: > users.id]
  rating int
  comment text
  created_at timestamptz [default: `now()`]
}
