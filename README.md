# 🛒 FastAPI E-Commerce Backend

A complete E-Commerce RESTful API backend built with **FastAPI**, **SQLAlchemy**, and **SQLite**. It supports user authentication, product catalog, cart management, order placement, and secure email-based password reset and verification using **Gmail SMTP** and **Mailpit**.

---

## 🚀 Features

- ✅ JWT-based Authentication with Access & Refresh Tokens
- ✅ Role-Based Access Control (RBAC): `user`, `admin`
- ✅ Password Hashing (bcrypt)
- ✅ Password Reset Flow with Expiry Tokens (UUID/JWT)
- ✅ User Signup with Email Verification (Gmail + Mailpit)
- ✅ Product CRUD for Admins
- ✅ Public Product Filtering, Search, and Sorting
- ✅ Cart Management (Add/Update/Delete/View)
- ✅ Order Placement with Dummy Checkout and Cart Clearance
- ✅ Structured Logging & Centralized Error Handling
- ✅ Pydantic Validation and Clean Schema-Model Mapping
- ✅ Modular Folder Structure with Dependency Injection

---
## 📁 Folder Structure

```bash
ecommerce-backend/
├── alembic/
│   └── versions/
├── app/
│   ├── auth/         # Login, Signup, Password Reset, JWT tokens
│   ├── users/        # User CRUD, role enforcement
│   ├── products/     # Product CRUD and public listing
│   ├── cart/         # Add, remove, update, view cart
│   ├── orders/       # Place and view orders
│   ├── checkout/     # Dummy payment + cart to order
│   ├── email/        # Mail sending via Mailpit and Gmail
│   ├── core/         # Config, logging, database setup
│   ├── models/       # SQLAlchemy models
│   ├── schemas/      # Pydantic schemas
│   ├── utils/        # Token & helper functions
│   └── main.py       # FastAPI app startup
├── seed_products.py
├── requirements.txt
├── .env
├── alembic.ini
└── README.md

```

---

## ⚙️ Tech Stack

| Category             | Tool / Library              |
|----------------------|-----------------------------|
| Backend Framework    | FastAPI                     |
| ORM & DB             | SQLAlchemy + PostgreSQL     |
| Authentication       | JWT                         |
| Password Hashing     | bcrypt                      |
| Validation           | Pydantic                    |
| Migrations           | Alembic                     |
| Web Server           | Uvicorn                     |
| Logging              | Python Logging Module       |
| Email                | Gmail SMTP + Mailpit        |

---

## 🧪 API Modules & Key Endpoints

### 🔐 Auth & User Module

| Endpoint                   | Method | Description                    |
|----------------------------|--------|--------------------------------|
| `/auth/signup`            | POST   | Register new user              |
| `/auth/signin`            | POST   | User login, return JWT tokens  |
| `/auth/forgot-password`   | POST   | Send reset link via email      |
| `/auth/reset-password`    | POST   | Reset password via token       |
| `/auth/logout`            | POST   | Logout & delete token records  |

### 📦 Product Module

| Endpoint                  | Method | Description                     |
|---------------------------|--------|---------------------------------|
| `/products/`             | GET    | Public list with filters        |
| `/products/search`       | GET    | Search by name/description      |
| `/products/`             | POST   | Create (admin only)             |
| `/products/{id}`         | PUT    | Update (owner only)             |
| `/products/{id}`         | DELETE | Delete (owner only)             |

### 🛒 Cart Module

| Endpoint                          | Method | Description                  |
|-----------------------------------|--------|------------------------------|
| `/cart/`                         | GET    | View cart                    |
| `/cart/add`                      | POST   | Add product to cart          |
| `/cart/update/{product_id}`      | PUT    | Update quantity              |
| `/cart/remove/{product_id}`      | DELETE | Remove from cart             |

### 📦 Orders & Checkout

| Endpoint             | Method | Description                          |
|----------------------|--------|--------------------------------------|
| `/checkout/`        | POST   | Checkout → create order              |
| `/orders/`          | GET    | Get user's own orders                |
| `/orders/{id}`      | GET    | Get order by ID (if user owns it)    |

---

## 📧 Email Integration

Supports both:

- 🔁 **Mailpit**: For local testing (`http://localhost:8025`)
- ✉️ **Gmail SMTP**: Real email delivery via Gmail

**Use Cases:**
- Send password reset tokens
- Send email verification link (on signup)
- Easily switch between both via `EMAIL_BACKEND` config

---

## 🛠️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/your-username/ecommerce-backend.git
cd ecommerce-backend

```
### 2. Create Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate


```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set environment variables
```bash
DATABASE_URL=sqlite:///./db.sqlite3
SECRET_KEY=your-secret
EMAIL_BACKEND=gmail   # or mailpit
MAIL_USERNAME=your@gmail.com
MAIL_PASSWORD=your-app-password
```

### 5. Run Alembic migrations
```bash
alembic upgrade head
```

### 6. Start the app
```bash
uvicorn app.main:app --reload
```


## 🔒 Security
Bcrypt password hashing

Secure token expiration (UUID + expiry timestamp)

Role-based access decorators

Input validation via Pydantic

Structured error logging

SQL injection prevention via SQLAlchemy ORM

---

## 📘 API Documentation

- Swagger UI: `http://localhost:8000/docs`

## 🧾 Database Tables

| Table Name              | Description                                |
| ----------------------- | ------------------------------------------ |
| users                   | Stores user info, roles, hashed passwords  |
| products                | Admin-managed product listings             |
| cart\_items             | User-specific cart item records            |
| orders                  | Orders placed by users                     |
| order\_items            | Items associated with each order           |
| password\_reset\_tokens | One-time secure tokens for password resets |
| user\_tokens            |Access & refresh tokens with expiration date|


---

## ✅ Manual Testing Checklist

 Signup, login, logout functionality

 Forgot password + reset password flow

 Admin: create, update, delete products

 Public: browse & search products

 Cart: add, update, remove items

 Checkout: place orders

 Orders: view history and order details

---

## 🙋 Author
Vidhi Jaiswal
B.Tech CSE
GitHub: @vidhijaiswal-2702
Email: vidhijais123@gmail.com

---