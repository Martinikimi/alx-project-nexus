from rest_framework import serializers
from .models import Payment
from orders.models import Order

class PaymentListSerializer(serializers.ModelSerializer):
    """Serializer for payment listings"""
    order_number = serializers.CharField(source='order.order_number', read_only=True)
    user_email = serializers.CharField(source='order.user.email', read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id', 'order_number', 'user_email', 'payment_method', 
            'amount', 'status', 'transaction_id', 'created_at'
        ]
        read_only_fields = ['amount', 'status', 'transaction_id']


class PaymentDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed payment view"""
    order_number = serializers.CharField(source='order.order_number', read_only=True)
    user_email = serializers.CharField(source='order.user.email', read_only=True)
    user_name = serializers.CharField(source='order.user.username', read_only=True)
    shipping_address = serializers.CharField(source='order.shipping_address', read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id', 'order', 'order_number', 'user_email', 'user_name',
            'payment_method', 'amount', 'status', 'transaction_id',
            'shipping_address', 'is_successful', 'can_refund',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'order', 'amount', 'status', 'transaction_id', 
            'is_successful', 'can_refund', 'created_at', 'updated_at'
        ]


class PaymentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating payments"""
    order_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Payment
        fields = ['order_id', 'payment_method']
    
    def validate_order_id(self, value):
        """Validate that order exists and is pending payment"""
        try:
            order = Order.objects.get(id=value)
            
            # Check if order already has a payment
            if hasattr(order, 'payment'):
                raise serializers.ValidationError("This order already has a payment.")
                
            # Check if order is in a valid state for payment
            if order.status not in ['pending', 'confirmed']:
                raise serializers.ValidationError(
                    "Cannot process payment for orders that are shipped, delivered, or cancelled."
                )
                
        except Order.DoesNotExist:
            raise serializers.ValidationError("Order not found.")
        
        return value
    
    def validate_payment_method(self, value):
        """Validate payment method is supported"""
        supported_methods = ['mpesa', 'card', 'paypal', 'bank']
        if value not in supported_methods:
            raise serializers.ValidationError(
                f"Payment method not supported. Choose from: {', '.join(supported_methods)}"
            )
        return value
    
    def create(self, validated_data):
        """Create payment with order amount"""
        order_id = validated_data.pop('order_id')
        order = Order.objects.get(id=order_id)
        
        payment = Payment.objects.create(
            order=order,
            payment_method=validated_data['payment_method'],
            amount=order.total_amount,  # Use order total
            status='pending'
        )
        
        return payment


class PaymentStatusSerializer(serializers.ModelSerializer):
    """Serializer for updating payment status (admin/webhook)"""
    class Meta:
        model = Payment
        fields = ['status', 'transaction_id']
    
    def validate_status(self, value):
        """Validate status transitions"""
        valid_transitions = {
            'pending': ['completed', 'failed', 'cancelled'],
            'completed': ['refunded'],
            'failed': ['pending'],  # Allow retry
            'refunded': [],
            'cancelled': []
        }
        
        current_status = self.instance.status if self.instance else None
        
        if current_status and value not in valid_transitions.get(current_status, []):
            raise serializers.ValidationError(
                f"Cannot change status from {current_status} to {value}"
            )
        
        return value
    
    def validate_transaction_id(self, value):
        """Validate transaction ID is provided for completed payments"""
        if self.initial_data.get('status') == 'completed' and not value:
            raise serializers.ValidationError(
                "Transaction ID is required for completed payments."
            )
        return value


class PaymentRefundSerializer(serializers.Serializer):
    """Serializer for payment refund requests"""
    reason = serializers.CharField(required=True)
    refund_amount = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        required=False
    )
    
    def validate_refund_amount(self, value):
        """Validate refund amount is positive and not more than payment amount"""
        if value and value <= 0:
            raise serializers.ValidationError("Refund amount must be greater than zero.")
        return value
    
    def validate(self, data):
        """Validate payment can be refunded"""
        payment = self.context['payment']
        
        if not payment.can_refund:
            raise serializers.ValidationError(
                "Only completed payments can be refunded."
            )
        
        refund_amount = data.get('refund_amount', payment.amount)
        if refund_amount > payment.amount:
            raise serializers.ValidationError(
                f"Refund amount cannot exceed original payment amount of {payment.amount}"
            )
        
        return data


class MockPaymentSerializer(serializers.Serializer):
    """Serializer for mock payment processing """
    success = serializers.BooleanField(default=True)
    transaction_id = serializers.CharField(required=False)
    
    def validate_transaction_id(self, value):
        """Generate transaction ID if not provided"""
        if not value:
            from django.utils import timezone
            import random
            value = f"TXN{timezone.now().strftime('%Y%m%d%H%M%S')}{random.randint(1000, 9999)}"
        return value