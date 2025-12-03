🛒 NexusStore - Premium E-Commerce Platform
A complete Django REST Framework e-commerce solution with modern frontend, JWT authentication, and high-performance database optimization.

📖 Introduction
NexusStore is a feature-rich eCommerce platform built with Django REST Framework for the backend and vanilla JavaScript for the frontend. It provides a complete online shopping experience with user authentication, product management, shopping cart functionality, and order processing.

Project Highlights:
Modern Tech Stack: Django 5.2 + PostgreSQL + Vanilla JavaScript

Dual Environment Support: Works seamlessly on both localhost for development/testing and Render for live deployment

Performance Optimized: Strategic database indexes for 20-40x faster queries

Comprehensive Features: Full e-commerce workflow from browsing to checkout

🚀 Features
✅ Implemented Features
User Authentication - JWT with refresh tokens and secure session management

Product & Category Management - Advanced filtering, search, and pagination

Shopping Cart - Real-time updates with persistent storage

Order System - Complete order processing workflow with status tracking

Review & Rating System - Verified purchase reviews only

User Profile Management - Comprehensive user data and order history

Admin Dashboard - Full content management interface

API Documentation - Interactive Swagger/Redoc documentation

Responsive Frontend - Single Page Application with smooth navigation

Database Optimization - Strategic indexes for high performance

🔜 Planned Features
Payment gateway integration (Stripe, M-Pesa)

Advanced email notifications with Resend API

Admin analytics dashboard

Product recommendations engine

🛠️ Tech Stack
Backend
Framework: Django 5.2 & Django REST Framework

Database: PostgreSQL with performance optimization

Authentication: JWT Authentication with Simple JWT

Documentation: DRF-YASG for automatic API documentation

Static Files: WhiteNoise for static file serving

Security: CORS Headers for frontend integration

Frontend
Language: Pure JavaScript (No frameworks - vanilla ES6+)

Styling: CSS3 with Flexbox/Grid and responsive design

Icons: Font Awesome icons

Storage: Local Storage for token management

Architecture: SPA Architecture with client-side routing

🌐 Deployment & Environment Setup
Important: Understanding Dual Environment Support
The application is designed to work in two environments:

1. Local Development/Testing Environment
Backend URL: http://127.0.0.1:8000

Purpose: For testing and development

Data Persistence: Data persists across sessions

Requirements: Django backend running locally

2. Render Production Environment ⚠️ FREE TIER LIMITATIONS
Live URL: https://alx-project-nexus-agn5.onrender.com

Purpose: Live deployment and demonstration

Limitations: Render's free tier has important constraints:

Ephemeral Storage: Database resets after inactivity or redeploy

Sleep Mode: App sleeps after 15 minutes of inactivity

Limited Resources: 512MB RAM, shared CPU

🔄 Managing Render Free Tier Limitations
Due to Render's free tier constraints, you need to reinitialize data when the app wakes up or after redeployment:

Step 1: Run Migrations (Required after each sleep/redeploy)
bash
# Access the migration endpoint
# This recreates database tables and indexes
curl -X GET https://alx-project-nexus-agn5.onrender.com/api/run-migrations/

# Or visit in browser:
https://alx-project-nexus-agn5.onrender.com/api/run-migrations/
Step 2: Re-add Products and Test Data
After migrations, you need to:

Create admin user through /admin/ interface

Add products via admin panel at /admin/products/product/

Add categories via admin panel at /admin/categories/category/

Create test users for demonstration

Step 3: Keep App Alive (Optional)
To prevent the app from sleeping during testing:

bash
# Use a simple ping service (external)
# Or manually visit the app every 10 minutes
📋 Project Setup Guide
Prerequisites
Python 3.8+

PostgreSQL (or SQLite for development)

Git

Step-by-Step Local Setup
1. Clone and Setup Environment
bash
# Clone the repository
git clone https://github.com/Martinikimi/alx-project-nexus.git
cd alx-project-nexus

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
2. Install Dependencies
bash
# Install Python packages
pip install -r requirements.txt
3. Database Configuration
bash
# For PostgreSQL (recommended):
# Create a PostgreSQL database named 'nexusstore'
# Update DATABASE_URL in your environment variables

# For SQLite (development):
# No additional setup needed - uses db.sqlite3 automatically
4. Environment Configuration
Create a .env file in the project root:

env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://username:password@localhost:5432/nexusstore
5. Database Setup
bash
# Run migrations to create database tables
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser
# Follow prompts to create admin account
6. Collect Static Files
bash
python manage.py collectstatic --noinput
7. Start Development Server
bash
# Start the Django development server
python manage.py runserver

# Application will be available at:
# Frontend: http://127.0.0.1:8000/
# API Docs: http://127.0.0.1:8000/swagger/
# Admin: http://127.0.0.1:8000/admin/
Testing Your Setup
Verify Backend API
bash
# Test API endpoints
curl http://127.0.0.1:8000/api/products/
curl http://127.0.0.1:8000/api/categories/
Verify Frontend
Open http://127.0.0.1:8000/ in your browser:

You should see the NexusStore homepage

Navigate to different sections (Products, Cart, Login)

Test Authentication
Click "Register" to create a new account

Login with your credentials

Verify you can access protected pages (Profile, Cart)

🌐 Deployment
Hosted on Render.com
Live Application: https://alx-project-nexus-agn5.onrender.com

API Documentation: https://alx-project-nexus-agn5.onrender.com/swagger/

Alternative Docs: https://alx-project-nexus-agn5.onrender.com/redoc/

⚠️ Critical Render Free Tier Notes
Data Resets: Database is ephemeral - data will be lost after inactivity or redeploy

Migration Required: Always run /api/run-migrations/ after app wakes up

Sleep Mode: App sleeps after 15 minutes of inactivity

Cold Starts: First request after sleep may take 30-60 seconds

For Persistent Data
Option A: Upgrade to Render's paid tier ($7-15/month)

Option B: Use localhost for consistent testing

Option C: Use external PostgreSQL database (Neon, Supabase, etc.)

🎯 Access Points
Development (Localhost)
🌐 Frontend Application: http://127.0.0.1:8000/

📚 API Documentation: http://127.0.0.1:8000/swagger/

📖 Alternative Docs: http://127.0.0.1:8000/redoc/

📊 Admin Panel: http://127.0.0.1:8000/admin/

Production (Render)
🌐 Live Application: https://alx-project-nexus-agn5.onrender.com

📚 API Documentation: https://alx-project-nexus-agn5.onrender.com/swagger/

🔧 Run Migrations: https://alx-project-nexus-agn5.onrender.com/api/run-migrations/

🔌 API Endpoints
Authentication
POST /api/auth/register/ - User registration

POST /api/auth/login/ - User login with JWT

GET /api/auth/profile/ - User profile

POST /api/auth/logout/ - User logout

Products & Categories
GET /api/products/ - List products with search/filter

GET /api/products/{id}/ - Product details

GET /api/categories/ - List categories

Shopping Cart
GET /api/cart/ - Get cart contents

POST /api/cart/add/ - Add item to cart

PUT /api/cart/update/{id}/ - Update cart item

DELETE /api/cart/remove/{id}/ - Remove from cart

Orders & Payments
GET /api/orders/ - Order history

POST /api/orders/ - Create new order

GET /api/orders/{id}/ - Order details

POST /api/payments/process/ - Process payment

Reviews
GET /api/reviews/ - Product reviews

POST /api/reviews/ - Create review

PUT /api/reviews/{id}/ - Update review

System Management (Render-specific)
GET /api/run-migrations/ - Run database migrations (essential for Render free tier)

🗃️ Database Design
The database uses a relational model optimized for e-commerce operations with proper indexing and relationships.

Key Tables:
users - User accounts and profiles

products - Product catalog with categories

categories - Product categorization with hierarchy

cart_items - Shopping cart management

orders & order_items - Order processing

payments - Payment transactions

reviews - Product reviews and ratings

Database Performance Optimization
Applied Optimizations:

12+ Strategic indexes across critical tables

Composite indexes for combined queries

Partial indexes for conditional filtering

Descending indexes for sorting performance

Apply Optimizations:

bash
# Apply all performance indexes
python manage.py migrate

# Verify index usage
python manage.py dbshell -- -c "SELECT indexname, indexdef FROM pg_indexes WHERE tablename = 'products';"
Performance Impact:

Product searches: 20-40x faster

Price filtering: 15-35x faster

User orders: 10-25x faster

Cart operations: 10-20x faster

🎨 Frontend Architecture
JavaScript Structure
Project Root (static/js/)

utils.js - Core utilities & API helpers

app.js - Main application initialization

auth.js - Authentication functions

products.js - Product listing & filtering

categories.js - Category management

cart.js - Shopping cart operations

orders.js - Order processing

Key Features Implemented
SPA Navigation - Smooth page transitions without reloads

API Integration - RESTful API communication with error handling

Real-time Updates - Cart counts, search results, user status

JWT Authentication - Secure token-based sessions

Responsive Design - Mobile-first approach

Loading States - Better user experience with feedback

Key Pages
Home - Featured products and categories

Products - Advanced filtering and search

Categories - Browse by product categories

Cart - Manage shopping cart items with quantity control

Checkout - Place orders with complete workflow

Profile - User account management

Orders - Order history and tracking

📚 API Documentation
Interactive Documentation
Our API is fully documented with auto-generated Swagger/OpenAPI documentation:

Swagger UI: /swagger/ - Interactive API testing

ReDoc: /redoc/ - Beautiful documentation reader

Documentation Features
✅ All endpoints with HTTP methods
✅ Request/Response schemas
✅ Authentication requirements
✅ Live API testing capabilities
✅ Code examples
✅ Automatic updates when code changes

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
python manage.py collectstatic --noinput
Testing
bash
# Run all tests
python manage.py test

# Test specific app
python manage.py test users

# Test with coverage
coverage run manage.py test
coverage report
📁 Project Structure
Project Root (alx-project-nexus/)

config/ - Django settings & URLs configuration

users/ - Authentication & user management app

products/ - Product catalog management app

categories/ - Category system with hierarchy app

cart/ - Shopping cart functionality app

orders/ - Order processing system app

reviews/ - Review & rating system app

payments/ - Payment integration models app

static/

css/ - Responsive stylesheets

js/ - JavaScript application files

templates/

emails/ - Email HTML templates

management/commands/ - Custom Django management commands

requirements.txt - Python dependencies

render.yaml - Render deployment configuration

manage.py - Django management script

🚀 Production Features
Ready for Production
Static files configured for production with WhiteNoise

Database optimization applied with strategic indexes

API documentation included with interactive interfaces

Frontend SPA fully functional with client-side routing

Security best practices implemented

Security Configuration
CORS configured for frontend-backend communication

CSRF protection with exemptions for API endpoints

HTTPS enforcement in production environment

Secure headers (HSTS, XSS Protection)

Input validation with Django serializers

Deployment Checklist
Set production environment variables

Configure database connection

Set up static file serving

Configure domain and SSL

Update CORS settings

Configure CSRF trusted origins

Set up automated deployments

🔒 Security Features
JWT Authentication with refresh tokens and blacklisting

CSRF Protection with exemptions for API endpoints

CORS Configuration for secure frontend integration

HTTPS Enforcement in production environment

Secure Headers (HSTS, XSS Protection)

Input Validation with Django serializers

Password Hashing with Django's built-in validators

📋 API Endpoints Reference
Authentication Endpoints
Endpoint	Method	Description	Authentication
/api/auth/register/	POST	User registration	None
/api/auth/login/	POST	User login with JWT tokens	None
/api/auth/profile/	GET	Get user profile	Required
/api/auth/logout/	POST	User logout with token blacklisting	Required
Product Endpoints
Endpoint	Method	Description	Authentication
/api/products/	GET	List all products with filtering	Optional
/api/products/	POST	Create new product	Admin
/api/products/{id}/	GET	Get product details	Optional
/api/products/{id}/	PUT	Update product	Admin
/api/products/{id}/	DELETE	Delete product	Admin
Cart Endpoints
Endpoint	Method	Description	Authentication
/api/cart/	GET	Get cart contents	Required
/api/cart/add/	POST	Add item to cart	Required
/api/cart/update/{id}/	PUT	Update cart item quantity	Required
/api/cart/remove/{id}/	DELETE	Remove item from cart	Required
Order Endpoints
Endpoint	Method	Description	Authentication
/api/orders/	GET	Get user's order history	Required
/api/orders/	POST	Create new order from cart	Required
/api/orders/{id}/	GET	Get order details	Required
/api/orders/{id}/cancel/	POST	Cancel order	Required
🛠️ Admin Guide
Accessing Admin Panel
URL: /admin/

Credentials: Use superuser account created during setup

Key Admin Features
User Management: View and manage user accounts

Product Catalog: Add, edit, and manage products

Category Management: Organize products into categories

Order Processing: View and process customer orders

Review Moderation: Manage product reviews and ratings

Product Management
Add new products with images and descriptions

Set pricing, inventory levels, and availability

Organize products into categories and subcategories

Manage product features and specifications

Order Management
View all customer orders with detailed information

Update order status throughout fulfillment process

Track order processing and shipping

Handle cancellations and customer service

🔄 Development Workflow
Adding New Features
Create new app or extend existing ones

Define models and serializers

Create API views and URL routes

Update frontend JavaScript for new functionality

Test thoroughly across different scenarios

Deploy to production environment

Code Quality
Follow Django and REST API best practices

Use consistent naming conventions

Implement proper error handling

Write comprehensive documentation

Test across multiple browsers and devices

⚠️ Known Limitations
Current Limitations
Data Persistence: Free Render tier may reset database on deploy/sleep

Email Service: Basic email setup (Resend API configured but limited sending)

Payment Processing: Payment models ready but no live gateway integration

File Uploads: Image upload functionality needs cloud storage setup

Workarounds
For demo purposes: Use localhost for consistent data persistence

For Render: Run migrations and add data after each wake-up

Email: Can be enhanced with full Resend API integration

Payments: Ready for Stripe/M-Pesa integration when needed

🐛 Troubleshooting
Common Issues & Solutions
Login/Authentication Issues
Ensure JWT tokens are properly stored in localStorage

Check CORS settings for frontend-backend communication

Verify CSRF exemptions for API endpoints

Database Performance
Ensure performance indexes are applied

Check query optimization with EXPLAIN ANALYZE

Monitor database connections and pooling

Static Files Not Loading
Run python manage.py collectstatic --noinput

Check WhiteNoise configuration in settings

Verify static file paths in production

API Documentation Errors
Check that drf-yasg is properly installed

Verify Swagger configuration in URLs

Ensure all API views have proper docstrings

Render Free Tier Issues
App Sleeping: Visit the app to wake it up (takes 30-60 seconds)

Data Lost: Always run /api/run-migrations/ after wake-up

Slow Response: First request after sleep is slower

Migration Required: Database resets - reinitialize data

📄 License
MIT License - feel free to use this project for learning, development, and commercial purposes.

📞 Support
For issues and questions:

Create an issue on GitHub

Check existing documentation

Review API documentation at /swagger/

💡 Testing Guide
For Most Reliable Testing Experience
Use the localhost setup for consistent testing:

bash
# 1. Start backend
python manage.py runserver

# 2. Open frontend
open http://127.0.0.1:8000/

# 3. Test all features with persistent data
This avoids Render's free tier limitations and provides a consistent testing environment.

Test Users for Local Setup
Admin: Use the superuser created during setup

Customer: Register a new account through the interface

Test Products: Add sample products through admin panel

Developed by Martin Ikimi - A complete eCommerce solution built with Django REST Framework and vanilla JavaScript.

