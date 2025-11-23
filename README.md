🛒 E-Commerce Backend API
A Django REST Framework e-commerce backend with JWT authentication, product management, and order processing.

🚀 Features
User Authentication (JWT)

Product & Category Management

Shopping Cart

Order System

API Documentation

🛠️ Tech Stack
Django & Django REST Framework

PostgreSQL

JWT Authentication

🗃️ Database Design
![ERD Diagram](/docs/erd.png)

📦 Installation
bash
git clone [your-repo]
cd ecommerce-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
🎯 Frontend
The frontend is a single-page application built with HTML, CSS, and JavaScript that provides a complete user interface for the e-commerce platform. It connects to the backend API and allows customers to browse products, manage their cart, place orders, and track purchases.

Frontend Features:

Modern responsive design

User authentication interface

Product catalog and shopping cart

Order management system

Mobile-friendly layout

To use the frontend:

Ensure the backend is running on http://127.0.0.1:8000

Open the index.html file in your web browser

The frontend will automatically connect to your backend API