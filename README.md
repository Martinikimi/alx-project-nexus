# 🛒 NexusStore - Premium E-Commerce Platform

A complete Django REST Framework e-commerce solution with modern frontend, JWT authentication, and high-performance database optimization.

## 🚀 Features

### Backend API
- **User Authentication** (JWT with refresh tokens)
- **Product & Category Management** with advanced filtering
- **Shopping Cart** with real-time updates
- **Order System** with status tracking
- **Payment Integration** (M-Pesa, PayPal, Stripe, Card)
- **Review & Rating System**
- **Admin Dashboard** with analytics
- **Email Notifications** with Resend API integration
- **CSRF-Exempt Authentication** for seamless frontend integration

### Frontend SPA
- **Modern Single-Page Application** (Pure HTML/CSS/JS)
- **Responsive Design** - Mobile-first approach
- **Real-time Search & Filtering**
- **Interactive Shopping Cart**
- **User Profile Management**
- **Order History & Tracking**
- **Order Confirmation Emails** with professional templates

### Performance
- **Database Optimization** with strategic indexes
- **Fast Product Search** with category filtering
- **Optimized API Responses** with pagination
- **Efficient Cart Operations**
- **Asynchronous Email Processing** with threading

## 🛠️ Tech Stack

### Backend
- **Django 4.2** & Django REST Framework
- **PostgreSQL** with performance optimization
- **JWT Authentication**
- **DRF-YASG** for automatic API documentation
- **Resend API** for email delivery
- **WhiteNoise** for static file serving

### Frontend
- **Pure JavaScript** (No frameworks)
- **CSS3** with Flexbox/Grid
- **Font Awesome** icons
- **Responsive Design**

## 📦 Installation & Setup

### Backend Setup
```bash
# Clone repository
git clone https://github.com/Martinikimi/alx-project-nexus.git
cd alx-project-nexus

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
Frontend Setup
The frontend is automatically served by Django. Just start the server and visit:

bash
python manage.py runserver
# Frontend available at: http://127.0.0.1:8000/
🎯 Access Points
Development
🌐 Frontend Application: http://127.0.0.1:8000/

📚 API Documentation: http://127.0.0.1:8000/swagger/

📖 Alternative Docs: http://127.0.0.1:8000/redoc/

📊 Admin Panel: http://127.0.0.1:8000/admin/

Production
🌐 Live Application: https://alx-project-nexus-agn5.onrender.com

📚 API Documentation: https://alx-project-nexus-agn5.onrender.com/swagger/

🔌 API Endpoints
Authentication: /api/auth/ (Login, Register, Profile)

Products: /api/products/ (Search, Filter, Categories)

Categories: /api/categories/

Cart: /api/cart/ (Add, Remove, Update)

Orders: /api/orders/ (Create, Track, Cancel)

Payments: /api/payments/ (Process, Webhooks)

Reviews: /api/reviews/ (Create, Rate, Helpful)

📧 Email System
Features
Order Confirmation emails to customers

Admin Notifications for new orders

Professional HTML Templates with branding

Asynchronous Processing for better performance

Resend API Integration for reliable delivery

Email Templates
Customer Confirmation (Green theme)

Admin Notification (Red theme with action buttons)

Order Status Updates

Shipping Notifications

🚀 Frontend Features
User Experience
Single-Page Navigation - No page reloads

Real-time Search - Instant product filtering

Category Browsing - Direct category-to-products navigation

Shopping Cart - Add/remove items with quantity control

Responsive Design - Works on all devices

Order Tracking - Real-time order status updates

Key Pages
Home - Featured products and categories

Products - Advanced filtering and search

Categories - Browse by product categories

Cart - Manage shopping cart items

Checkout - Place orders with shipping address

Profile - User account management

Orders - Order history and tracking

🗃️ Database Design
The database uses a relational model optimized for e-commerce operations with proper indexing and relationships.

Key Tables:
users - User accounts and profiles

products - Product catalog with categories

categories - Product categorization

cart_items - Shopping cart management

orders & order_items - Order processing

payments - Payment transactions

reviews - Product reviews and ratings

🗃️ Database Performance Optimization
Applied Optimizations
12 Strategic Indexes across critical tables

Composite Indexes for combined queries

Partial Indexes for conditional filtering

Descending Indexes for sorting performance

Apply Optimizations
bash
# Apply all performance indexes
python manage.py migrate

# Verify index usage
python manage.py dbshell -- -c "SELECT indexname, indexdef FROM pg_indexes WHERE tablename = 'products';"
Performance Impact
Product searches: 20-40x faster

Price filtering: 15-35x faster

User orders: 10-25x faster

Cart operations: 10-20x faster

📚 API Documentation
Interactive Documentation
Our API is fully documented with auto-generated Swagger/OpenAPI documentation:

Swagger UI: https://alx-project-nexus-agn5.onrender.com/swagger/ - Interactive API testing

ReDoc: https://alx-project-nexus-agn5.onrender.com/redoc/ - Beautiful documentation reader

Documentation Features
✅ All endpoints with HTTP methods

✅ Request/Response schemas

✅ Authentication requirements

✅ Live API testing

✅ Code examples

✅ Automatic updates when code changes

🎨 Frontend Architecture
JavaScript Structure
text
static/js/
├── utils.js          # Core utilities & API helpers
├── app.js            # Main application initialization
├── auth.js           # Authentication functions
├── products.js       # Product listing & filtering
├── categories.js     # Category management
├── cart.js           # Shopping cart operations
└── orders.js         # Order processing
Key Features Implemented
SPA Navigation - Smooth page transitions

API Integration - RESTful API communication

Real-time Updates - Cart counts, search results

Error Handling - User-friendly error messages

Loading States - Better user experience

Token-based Authentication - Secure user sessions

🔧 Development Commands
Database Operations
bash
# Apply migrations
python manage.py migrate

# Create new migration
python manage.py makemigrations

# Check database performance
python manage.py dbshell -- -c "EXPLAIN ANALYZE SELECT * FROM products WHERE name LIKE 'iPhone%';"
Frontend Development
bash
# Start development server
python manage.py runserver

# Collect static files (production)
python manage.py collectstatic
Email Testing
bash
# Test email functionality
python manage.py shell -c "from orders.utils import send_test_email; send_test_email()"
📁 Project Structure
text
alx-project-nexus/
├── config/              # Django settings
├── users/               # Authentication app
├── products/            # Product management
├── categories/          # Category system
├── cart/                # Shopping cart
├── orders/              # Order processing & email utils
├── reviews/             # Review system
├── payments/            # Payment integration
├── static/
│   ├── css/            # Stylesheets
│   └── js/             # JavaScript files
├── templates/
│   └── emails/         # Email HTML templates
├── database/           # Performance optimizations
├── scripts/            # Utility scripts
└── manage.py
🚀 Deployment Ready
Production Features
Static files configured for production

Database optimization applied

API documentation included

Frontend SPA fully functional

Security best practices implemented

Email system with Resend API

CSRF protection with exemptions for API endpoints

Deployment Checklist
Set production environment variables

Configure database connection

Set up static file serving

Configure domain and SSL

Update CORS settings

Set up email service (Resend API)

Configure CSRF trusted origins

🔒 Security Features
JWT Authentication with refresh tokens

CSRF Protection with exemptions for API endpoints

CORS Configuration for frontend integration

HTTPS Enforcement in production

Secure Headers (HSTS, XSS Protection)

Input Validation with Django serializers

📄 License
MIT License - feel free to use this project for learning and development.