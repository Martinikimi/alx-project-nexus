from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from .models import Order, OrderItem
from .serializers import (
    OrderListSerializer,
    OrderDetailSerializer,
    OrderCreateSerializer,
    OrderStatusSerializer,
    OrderCancelSerializer
)
from cart.models import Cart

class OrderListView(generics.ListAPIView):
    """
    Get user's order history
    - User must be logged in
    - Only shows user's own orders
    """
    serializer_class = OrderListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users can only see their own orders
        return Order.objects.filter(user=self.request.user).order_by('-created_at')


class OrderDetailView(generics.RetrieveAPIView):
    """
    Get order details
    - User must be logged in
    - Users can only see their own orders
    """
    serializer_class = OrderDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users can only see their own orders
        return Order.objects.filter(user=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_order(request):
    """
    Create order from user's cart
    - User must be logged in
    - Requires shipping address
    - Clears cart after successful order
    """
    # Check if user has a cart with items
    cart = get_object_or_404(Cart, user=request.user)
    
    if not cart.items.exists():
        return Response(
            {"error": "Cart is empty. Add items to cart before placing an order."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    serializer = OrderCreateSerializer(data=request.data)
    
    if serializer.is_valid():
        shipping_address = serializer.validated_data['shipping_address']
        
        try:
            # Use your model's create_from_cart method
            order = Order.create_from_cart(cart, shipping_address)
            
            return Response(
                {
                    "message": "Order created successfully",
                    "order_number": order.order_number,
                    "order_id": order.id
                },
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            return Response(
                {"error": f"Failed to create order: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def cancel_order(request, order_id):
    """
    Cancel order
    - User must be logged in
    - Users can only cancel their own orders
    - Only pending/confirmed orders can be cancelled
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    serializer = OrderCancelSerializer(
        data=request.data, 
        context={'order': order}
    )
    
    if serializer.is_valid():
        # Update order status to cancelled
        order.status = 'cancelled'
        order.save()
        
        return Response(
            {"message": "Order cancelled successfully"},
            status=status.HTTP_200_OK
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminOrderListView(generics.ListAPIView):
    """
    Get all orders (Admin only)
    - Admin users only
    - Shows all orders in the system
    """
    serializer_class = OrderListSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Order.objects.all().order_by('-created_at')


class AdminOrderDetailView(generics.RetrieveAPIView):
    """
    Get order details (Admin only)
    - Admin users only
    - Can view any order
    """
    serializer_class = OrderDetailSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Order.objects.all()


class AdminOrderStatusView(generics.UpdateAPIView):
    """
    Update order status (Admin only)
    - Admin users only
    - Validates status transitions
    """
    serializer_class = OrderStatusSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Order.objects.all()
