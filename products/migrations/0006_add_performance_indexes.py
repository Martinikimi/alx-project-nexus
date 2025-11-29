from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('products', '0005_alter_product_sku'),
    ]

    operations = [
        migrations.RunSQL("""
            CREATE INDEX IF NOT EXISTS idx_products_name ON products_product(name);
            CREATE INDEX IF NOT EXISTS idx_products_price ON products_product(price);
            CREATE INDEX IF NOT EXISTS idx_products_created_at ON products_product(created_at DESC);
            CREATE INDEX IF NOT EXISTS idx_products_is_featured ON products_product(is_featured) WHERE is_featured = true;
            CREATE INDEX IF NOT EXISTS idx_products_is_active ON products_product(is_active) WHERE is_active = true;
            CREATE INDEX IF NOT EXISTS idx_products_stock_quantity ON products_product(stock_quantity) WHERE stock_quantity > 0;
        """)
    ]