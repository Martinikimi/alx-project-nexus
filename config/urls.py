from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView 
from django.conf import settings
from django.conf.urls.static import static

# Swagger imports
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

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
    
    # Serve index.html for frontend routes
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('login/', TemplateView.as_view(template_name='index.html'), name='login'),
    path('register/', TemplateView.as_view(template_name='index.html'), name='register'),
    path('profile/', TemplateView.as_view(template_name='index.html'), name='profile'),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Catch-all route AFTER static configuration
urlpatterns += [
    path('<path:unknown_path>/', TemplateView.as_view(template_name='index.html')),
]