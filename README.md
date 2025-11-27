# 🛒 E-Commerce Backend API

A Django REST Framework e-commerce backend with JWT authentication, product management, and order processing.

## 🚀 Features
- User Authentication (JWT)
- Product & Category Management  
- Shopping Cart
- Order System
- API Documentation
- **Database Performance Optimization** (NEW)

## 🛠️ Tech Stack
- Django & Django REST Framework
- PostgreSQL
- JWT Authentication

🗃️ Database Design
![ERD Diagram](/docs/erd.png)

## 📦 Installation
```bash
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

🚀 Database Performance Optimization
Overview
This project includes comprehensive database optimization strategies to ensure high-performance query execution, especially for product searches, user orders, and shopping cart operations.

What We Implemented:
Strategic Database Indexes - 12 performance indexes across critical tables

Automated Index Application - Python script for easy setup

Comprehensive Documentation - Full optimization strategy and verification methods

Performance Indexes Applied:
Products Table: Name search, price filtering, category filtering, featured products, date sorting, composite searches

Orders Table: User order lookup, date sorting, composite user-date queries

Cart & Orders: User cart retrieval, order item lookup

Reviews: Product review display optimization

Apply Database Optimizations:
bash
# Apply all performance indexes with one command
python scripts/database_indexes.py
Expected Performance Impact:
Based on database optimization principles, these indexes transform slow sequential scans into fast index-based queries:

Product searches: 20-40x faster (reducing from seconds to milliseconds)

Price & category filtering: 15-35x faster

User order history: 10-25x faster

Shopping cart operations: 10-20x faster

Reviews display: 15-30x faster

Verify Optimization:
sql
-- Check if indexes are being used in queries
EXPLAIN ANALYZE SELECT * FROM products WHERE name LIKE 'wireless%';

-- View all created indexes
SELECT indexname, indexdef FROM pg_indexes WHERE tablename = 'products';

-- Monitor index usage statistics
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes WHERE tablename = 'products';
Optimization Files:
database/migrations/002_performance_indexes.sql - All index definitions

scripts/database_indexes.py - Automated application script

database/optimization_docs.md - Complete optimization documentation

Key Optimization Strategies:
Composite Indexes for frequently combined queries (name + category + price)

Partial Indexes for conditional queries (featured products, in-stock items)

Descending Indexes for "newest first" sorting

Foreign Key Indexes for relationship-based queries

📁 Project Structure
text
ecommerce-backend/
├── config/             
├── users/                  
├── products/               
├── categories/             
├── cart/                   
├── orders/                 
├── reviews/              
├── payments/               
├── common/               
├── database/              
│   ├── migrations/
│   │   └── 002_performance_indexes.sql
│   └── optimization_docs.md
├── scripts/                
│   └── database_indexes.py
├── static/                
├── media/                  
├── templates/           
├── docs/                  
├── manage.py
├── requirements.txt
├── docker-compose.yml
└── README.md
🔧 Development
Backend API
API Base URL: http://127.0.0.1:8000/api

Admin Interface: http://127.0.0.1:8000/admin

API Documentation: Available at /api/docs/

Database Optimization Commands
bash
# Apply performance indexes
python scripts/database_indexes.py

# Check index usage
python manage.py dbshell -- -c "SELECT indexname, indexdef FROM pg_indexes WHERE tablename = 'products';"

# Monitor performance
python manage.py dbshell -- -c "EXPLAIN ANALYZE SELECT * FROM products WHERE name LIKE 'iPhone%';"
📊 Performance Monitoring
Regularly monitor database performance using:

Django Debug Toolbar for development

PostgreSQL query logs

Index usage statistics

EXPLAIN ANALYZE for slow queries

🛠️ Maintenance
Database Maintenance
sql
-- Update table statistics for query planner
ANALYZE products;

-- Regular vacuum maintenance
VACUUM ANALYZE products;

-- Monitor unused indexes
SELECT schemaname, tablename, indexname
FROM pg_stat_user_indexes 

WHERE idx_scan = 0;

WHERE idx_scan = 0;
📄 License

