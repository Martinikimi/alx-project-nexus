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

# HEALTH CHECK
def health_check(request):
    try:
        from django.db import connection
        connection.ensure_connection()
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return JsonResponse({"status": "ok", "database": db_status, "debug": settings.DEBUG})

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
    path('api/health/', health_check),
    
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