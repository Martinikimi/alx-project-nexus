from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('orders', '0002_initial'),
    ]

    operations = [
        migrations.RunSQL("""
            -- USERS OPTIMIZATION
            CREATE INDEX IF NOT EXISTS idx_users_email ON users_user(email);
            
            -- PRODUCTS TABLE OPTIMIZATION
            CREATE INDEX IF NOT EXISTS idx_products_name ON products_product(name);
            CREATE INDEX IF NOT EXISTS idx_products_price ON products_product(price);
            CREATE INDEX IF NOT EXISTS idx_products_created_at ON products_product(created_at DESC);
            
            -- ORDERS TABLE OPTIMIZATION
            CREATE INDEX IF NOT EXISTS idx_orders_created_at ON orders_order(created_at DESC);
            CREATE INDEX IF NOT EXISTS idx_orders_status ON orders_order(status);
            CREATE INDEX IF NOT EXISTS idx_orders_user_date_composite ON orders_order(user_id, created_at DESC);
            
            -- CART OPTIMIZATION
            CREATE INDEX IF NOT EXISTS idx_cart_items_cart_id ON cart_cartitem(cart_id);
            CREATE INDEX IF NOT EXISTS idx_cart_items_product_id ON cart_cartitem(product_id);
            
            -- ORDER ITEMS OPTIMIZATION
            CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON orders_orderitem(order_id);
            CREATE INDEX IF NOT EXISTS idx_order_items_product_id ON orders_orderitem(product_id);
        """)
    ]