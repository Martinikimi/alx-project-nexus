from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView 
from django.conf import settings
from django.http import JsonResponse  
from django.views.static import serve
from django.core.management import call_command

# Swagger imports
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# MIGRATION FUNCTION
def run_migrations(request):
    try:
        call_command('migrate', verbosity=0)
        return JsonResponse({"status": "success", "message": "All migrations completed successfully"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e), "error_type": type(e).__name__}, status=500)

# TEST EMAIL FUNCTION
def test_email(request):
    from django.core.mail import send_mail
    try:
        send_mail(
            'Test Email from Your Store',
            'This is a test email from your Django application.',
            'martinikimi7@gmail.com',
            ['martinikimi7@gmail.com'],
            fail_silently=False,
        )
        return JsonResponse({"status": "success", "message": "Test email sent!"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

# HEALTH CHECK
def health_check(request):
    try:
        from django.db import connection
        connection.ensure_connection()
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return JsonResponse({"status": "ok", "database": db_status, "debug": settings.DEBUG})

# SAFE DIAGNOSTIC FUNCTIONS -
def safe_debug_products(request):
    try:
        from django.db import connection
        
        Try to access products table directly
        with connection.cursor() as cursor:
            # Method 1: Simple table existence check
            try:
                cursor.execute("SELECT 1 FROM products_product LIMIT 1")
                table_exists = True
            except:
                table_exists = False
            
            # Method 2: Count products if table exists
            if table_exists:
                cursor.execute("SELECT COUNT(*) FROM products_product")
                product_count = cursor.fetchone()[0]
            else:
                product_count = 0
        
        return JsonResponse({
            "products_table_exists": table_exists,
            "product_count": product_count,
            "safe_check": True
        })
        
    except Exception as e:
        return JsonResponse({
            "error": str(e),
            "error_type": type(e).__name__
        }, status=500)

def check_migration_status(request):
    try:
        from django.db import connection
        from django.core.management.color import no_style
        from django.db.migrations.loader import MigrationLoader
        
        loader = MigrationLoader(connection)
        applied_migrations = loader.applied_migrations
        planned_migrations = loader.graph.leaf_nodes()
        
        # Get unapplied migrations
        unapplied = [mig for mig in planned_migrations if mig not in applied_migrations]
        
        return JsonResponse({
            "applied_migrations_count": len(applied_migrations),
            "unapplied_migrations_count": len(unapplied),
            "unapplied_migrations": [str(mig) for mig in unapplied],
            "has_products_app": 'products' in loader.migrated_apps
        })
        
    except Exception as e:
        return JsonResponse({
            "error": str(e),
            "error_type": type(e).__name__
        }, status=500)

# Schema view for Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="NexusStore API",
        default_version='v1',
        description="Premium E-Commerce Backend API",
        terms_of_service="https://www.nexusstore.com/terms/",
        contact=openapi.Contact(email="support@nexusstore.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # MIGRATION ENDPOINT
    path('api/run-migrations/', run_migrations),
    
    # TEST ENDPOINTS 
    path('api/test-email/', test_email),  
    path('api/health/', health_check),
    
    # NEW DIAGNOSTIC ENDPOINTS 
    path('api/debug/safe-products/', safe_debug_products),
    path('api/debug/migration-status/', check_migration_status),
    
    # API Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # API Routes
    path('api/auth/', include('users.urls')), 
    path('api/categories/', include('categories.urls')),
    path('api/products/', include('products.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/reviews/', include('reviews.urls')),
    path('api/payments/', include('payments.urls')), 
    
    # Serve static files
    path('static/<path:path>', serve, {'document_root': settings.STATIC_ROOT}),
    
    # Serve media files 
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
    
    # Serve index.html for frontend routes
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('login/', TemplateView.as_view(template_name='index.html'), name='login'),
    path('register/', TemplateView.as_view(template_name='index.html'), name='register'),
    path('profile/', TemplateView.as_view(template_name='index.html'), name='profile'),
]

# Catch-all route should be ABSOLUTELY LAST
urlpatterns += [
    path('<path:unknown_path>/', TemplateView.as_view(template_name='index.html')),
]