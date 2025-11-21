from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    # Cart management
    path('', views.CartDetailView.as_view(), name='cart-detail'),
    path('add/', views.add_to_cart, name='add-to-cart'),
    path('clear/', views.clear_cart, name='clear-cart'),
    
    # Cart item operations
    path('items/<int:item_id>/increase/', views.increase_cart_item, name='increase-item'),
    path('items/<int:item_id>/decrease/', views.decrease_cart_item, name='decrease-item'),
    path('items/<int:pk>/update/', views.UpdateCartItemView.as_view(), name='update-item'),
    path('items/<int:pk>/remove/', views.RemoveCartItemView.as_view(), name='remove-item'),
]