from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('products', '0006_add_performance_indexes'),
    ]

    operations = [
        migrations.RunSQL("""
            -- USERS INDEXES
            CREATE INDEX IF NOT EXISTS idx_users_email ON users_user(email);
            
            -- ORDERS INDEXES
            CREATE INDEX IF NOT EXISTS idx_orders_created_at ON orders_order(created_at DESC);
            CREATE INDEX IF NOT EXISTS idx_orders_status ON orders_order(status);
            CREATE INDEX IF NOT EXISTS idx_orders_user_date_composite ON orders_order(user_id, created_at DESC);
            
            -- CART INDEXES
            CREATE INDEX IF NOT EXISTS idx_cart_items_cart_id ON cart_cartitem(cart_id);
            CREATE INDEX IF NOT EXISTS idx_cart_items_product_id ON cart_cartitem(product_id);
            
            -- ORDER ITEMS INDEXES
            CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON orders_orderitem(order_id);
            CREATE INDEX IF NOT EXISTS idx_order_items_product_id ON orders_orderitem(product_id);
            
            -- REVIEWS INDEXES
            CREATE INDEX IF NOT EXISTS idx_reviews_product_id ON reviews_review(product_id);
            CREATE INDEX IF NOT EXISTS idx_reviews_created_at ON reviews_review(created_at DESC);
        """)
    ]
