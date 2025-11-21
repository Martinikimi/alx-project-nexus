from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from .serializers import (CartSerializer,CartItemSerializer,CartAddSerializer,CartUpdateSerializer)
from products.models import Product


class CartDetailView(generics.RetrieveAPIView):
    """
    Get user's cart with all items
    - User must be logged in
    - Automatically creates cart if doesn't exist
    """
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Get or create cart for the current user
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_to_cart(request):
    """
    Add item to cart or increase quantity if already exists
    - User must be logged in
    - Creates cart if doesn't exist
    """
    serializer = CartAddSerializer(data=request.data)
    
    if serializer.is_valid():
        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data['quantity']
        
        # Get or create user's cart
        cart, created = Cart.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, id=product_id, is_active=True)
        
        # Check if item already in cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            # Item exists - increase quantity
            cart_item.quantity += quantity
            cart_item.save()
        
        return Response({"message": "Product added to cart"}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def increase_cart_item(request, item_id):
    """
    Increase cart item quantity by 1
    - User must be logged in
    - Must own the cart item
    """
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    # Increase quantity
    cart_item.quantity += 1
    cart_item.save()
    
    return Response({"message": "Quantity increased", "quantity": cart_item.quantity})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def decrease_cart_item(request, item_id):
    """
    Decrease cart item quantity by 1
    - If quantity becomes 0, remove item from cart
    - User must be logged in
    - Must own the cart item
    """
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if cart_item.quantity > 1:
        # Decrease quantity
        cart_item.quantity -= 1
        cart_item.save()
        return Response({"message": "Quantity decreased", "quantity": cart_item.quantity})
    else:
        # Remove item if quantity becomes 0
        cart_item.delete()
        return Response({"message": "Item removed from cart"})


class UpdateCartItemView(generics.UpdateAPIView):
    """
    Update cart item quantity (set exact amount)
    - User must be logged in
    - Must own the cart item
    """
    serializer_class = CartUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users can only update their own cart items
        return CartItem.objects.filter(cart__user=self.request.user)


class RemoveCartItemView(generics.DestroyAPIView):
    """
    Remove item from cart completely
    - User must be logged in
    - Must own the cart item
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users can only remove their own cart items
        return CartItem.objects.filter(cart__user=self.request.user)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def clear_cart(request):
    """
    Remove all items from cart
    - User must be logged in
    """
    cart = get_object_or_404(Cart, user=request.user)
    cart.items.all().delete()
    
    return Response({"message": "Cart cleared"})
