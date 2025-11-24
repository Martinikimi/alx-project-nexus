#!/usr/bin/env python3
"""
Database Index Optimization Script
"""

import os
import sys
import django
import psycopg2
from django.conf import settings

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def apply_database_indexes():
    try:
        sql_file_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'database', 'migrations', '002_performance_indexes.sql'
        )
        
        with open(sql_file_path, 'r') as file:
            sql_commands = file.read()
        
        conn = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT']
        )
        cursor = conn.cursor()
        
        print("🔄 Applying database performance indexes...")
        cursor.execute(sql_commands)
        conn.commit()
        
        print("✅ Database indexes applied successfully!")
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error applying indexes: {e}")
        sys.exit(1)

if __name__ == "__main__":
    apply_database_indexes()