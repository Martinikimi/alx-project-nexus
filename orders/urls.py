from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # User endpoints
    path('', views.OrderListView.as_view(), name='order-list'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('create/', views.create_order, name='create-order'),
    path('<int:order_id>/cancel/', views.cancel_order, name='cancel-order'),
    
    # Admin endpoints
    path('admin/all/', views.AdminOrderListView.as_view(), name='admin-order-list'),
    path('admin/<int:pk>/', views.AdminOrderDetailView.as_view(), name='admin-order-detail'),
    path('admin/<int:pk>/status/', views.AdminOrderStatusView.as_view(), name='admin-order-status'),
]