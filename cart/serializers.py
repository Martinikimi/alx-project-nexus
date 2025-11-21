from rest_framework import serializers
from .models import Cart, CartItem
from products.models import Product

class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for individual cart items"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', read_only=True, max_digits=10, decimal_places=2)
    item_total = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'product_price', 'quantity', 'item_total', 'added_at']
        read_only_fields = ['item_total', 'added_at']
    
    def get_item_total(self, obj):
        """Calculate total for this cart item (product.price * quantity)"""
        return obj.quantity * obj.product.price


class CartSerializer(serializers.ModelSerializer):
    """Serializer for full cart with items and totals"""
    items = CartItemSerializer(many=True, read_only=True)
    cart_total = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'cart_total', 'total_items', 'created_at', 'updated_at']
        read_only_fields = ['user', 'cart_total', 'total_items']
    
    def get_cart_total(self, obj):
        """Calculate total cost of all items in cart"""
        return sum(item.quantity * item.product.price for item in obj.items.all())
    
    def get_total_items(self, obj):
        """Calculate total number of items in cart"""
        return sum(item.quantity for item in obj.items.all())


class CartAddSerializer(serializers.Serializer):
    """Serializer for adding items to cart"""
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1, min_value=1)
    
    def validate_product_id(self, value):
        """Validate that product exists and is active"""
        try:
            product = Product.objects.get(id=value, is_active=True)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found or not available.")
        return value


class CartUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating cart item quantities"""
    class Meta:
        model = CartItem
        fields = ['quantity']
    
    def validate_quantity(self, value):
        """Validate quantity is positive"""
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value