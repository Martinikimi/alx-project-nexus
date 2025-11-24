from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
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

# Media serving BEFORE the catch-all route
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Catch-all route AFTER media configuration
urlpatterns += [
    path('<path:unknown_path>/', TemplateView.as_view(template_name='index.html')),
]