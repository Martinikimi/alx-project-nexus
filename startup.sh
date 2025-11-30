#!/bin/bash
# Wait for database to be ready, then run migrations, then start server
echo "Waiting for database to be ready..."
python manage.py migrate
echo "Migrations completed successfully"
python manage.py runserver 0.0.0.0:8000