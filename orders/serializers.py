from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductListSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for individual order items"""
    product = ProductListSerializer(read_only=True)
    item_total = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price', 'item_total']
        read_only_fields = ['price', 'item_total']
    
    def get_item_total(self, obj):
        """Calculate total for this order item"""
        return obj.quantity * obj.price


class OrderListSerializer(serializers.ModelSerializer):
    """Serializer for order listings (basic info)"""
    total_items = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'total_amount', 'status', 
            'created_at', 'total_items'
        ]
        read_only_fields = ['order_number', 'total_amount', 'status']
    
    def get_total_items(self, obj):
        """Calculate total number of items in order"""
        return sum(item.quantity for item in obj.items.all())


class OrderDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed order view"""
    items = OrderItemSerializer(many=True, read_only=True)
    total_items = serializers.SerializerMethodField()
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'user', 'user_email', 'total_amount',
            'shipping_address', 'status', 'items', 'total_items', 'created_at'
        ]
        read_only_fields = [
            'order_number', 'user', 'total_amount', 'status', 'created_at'
        ]
    
    def get_total_items(self, obj):
        """Calculate total number of items in order"""
        return sum(item.quantity for item in obj.items.all())


class OrderCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating orders from cart"""
    class Meta:
        model = Order
        fields = ['shipping_address']
    
    def validate_shipping_address(self, value):
        """Validate shipping address is provided"""
        if not value or len(value.strip()) < 10:
            raise serializers.ValidationError("Please provide a complete shipping address.")
        return value.strip()


class OrderStatusSerializer(serializers.ModelSerializer):
    """Serializer for updating order status (admin only)"""
    class Meta:
        model = Order
        fields = ['status']
    
    def validate_status(self, value):
        """Validate status transitions"""
        valid_transitions = {
            'pending': ['confirmed', 'cancelled'],
            'confirmed': ['shipped', 'cancelled'],
            'shipped': ['delivered'],
            'delivered': [],
            'cancelled': []
        }
        
        current_status = self.instance.status if self.instance else None
        
        if current_status and value not in valid_transitions.get(current_status, []):
            raise serializers.ValidationError(
                f"Cannot change status from {current_status} to {value}"
            )
        
        return value


class OrderCancelSerializer(serializers.Serializer):
    """Serializer for order cancellation"""
    reason = serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, data):
        """Validate order can be cancelled"""
        order = self.context['order']
        
        if order.status not in ['pending', 'confirmed']:
            raise serializers.ValidationError(
                "Order can only be cancelled while pending or confirmed."
            )
        
        return data