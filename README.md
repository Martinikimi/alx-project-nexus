# 🛒 E-Commerce Backend API

A production-ready Django REST Framework e-commerce backend with JWT authentication, complete product management, and order processing system.

## 🚀 Features
- ✅ User Authentication (JWT) 
- ✅ Product & Category Management with hierarchical categories
- ✅ Shopping Cart with session management
- ✅ Order System with status tracking
- ✅ Payment Processing with multiple methods
- ✅ Product Reviews & Ratings
- ✅ Admin Dashboard
- 🔄 API Documentation (Swagger/OpenAPI) - Coming soon\

## 🚀 Features
- ✅ User Authentication (JWT)
- ✅ Product & Category Management  
- ✅ Shopping Cart 
- ✅ **Order System with Auto-Checkout** ✅
- 🔄 API Documentation (Coming soon)

## 🛠️ Tech Stack
- **Backend**: Django & Django REST Framework
- **Database**: PostgreSQL 
- **Authentication**: JWT (SimpleJWT)
- **Image Handling**: Pillow
- **API Docs**: Swagger/OpenAPI (planned)

## 🗃️ Database Design
![ERD Diagram](/docs/erd.png)

## 📦 Installation & Setup

```bash
# Clone repository
git clone https://github.com/yourusername/ecommerce-backend.git
cd ecommerce-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database credentials

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver