from django.urls import path
from . import views

app_name = 'categories'

urlpatterns = [
    # Public endpoints
    path('', views.CategoryListView.as_view(), name='category-list'),
    path('<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    
    # Admin endpoints 
    path('create/', views.CategoryCreateView.as_view(), name='category-create'),
    path('<int:pk>/update/', views.CategoryUpdateView.as_view(), name='category-update'),
    path('<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category-delete'),
    
    # Admin-only complete list
    path('admin/all/', views.CategoryAdminListView.as_view(), name='category-admin-list'),
]