from django.db import migrations

def read_sql_file():
    try:
        with open('002_performance_indexes.sql', 'r') as f:
            return f.read()
    except FileNotFoundError:
        # Fallback SQL
        return """
        CREATE INDEX IF NOT EXISTS idx_orders_created_at ON orders_order(created_at DESC);
        CREATE INDEX IF NOT EXISTS idx_orders_status ON orders_order(status);
        """

class Migration(migrations.Migration):
    dependencies = [
        ('orders', '0002_initial'),
    ]

    operations = [
        migrations.RunSQL(read_sql_file())
    ]