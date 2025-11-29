from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Debug endpoint (to find the error)
    path('debug/', views.debug_test, name='debug-test'),
    
    # Public endpoints (anyone can access)
    path('', views.ProductListView.as_view(), name='product-list'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('category/<int:category_id>/', views.CategoryProductsView.as_view(), name='category-products'),
    path('featured/', views.FeaturedProductsView.as_view(), name='featured-products'),
    path('search/', views.ProductSearchView.as_view(), name='product-search'),
    
    # Admin endpoints (admin users only)
    path('create/', views.ProductCreateView.as_view(), name='product-create'),
    path('<int:pk>/update/', views.ProductUpdateView.as_view(), name='product-update'),
    path('<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product-delete'),
]