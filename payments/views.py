from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from .models import Payment
from .serializers import (
    PaymentListSerializer,
    PaymentDetailSerializer,
    PaymentCreateSerializer,
    PaymentStatusSerializer,
    PaymentRefundSerializer,
    MockPaymentSerializer
)
from orders.models import Order

class UserPaymentsListView(generics.ListAPIView):
    """
    Get user's payment history
    - User must be logged in
    - Only shows payments for user's own orders
    """
    serializer_class = PaymentListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users can only see payments for their own orders
        return Payment.objects.filter(
            order__user=self.request.user
        ).select_related('order', 'order__user').order_by('-created_at')


class PaymentDetailView(generics.RetrieveAPIView):
    """
    Get payment details
    - User must be logged in
    - Users can only see their own payments
    """
    serializer_class = PaymentDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users can only see their own payments
        return Payment.objects.filter(order__user=self.request.user)


class CreatePaymentView(generics.CreateAPIView):
    """
    Create payment for an order
    - User must be logged in
    - Can only create payment for their own orders
    - Order must not already have a payment
    """
    serializer_class = PaymentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        
        payment = serializer.save()
        
    


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def process_mock_payment(request, payment_id):
    """
    Process mock payment (for development only)
    - User must be logged in
    - Can only process their own payments
    - Simulates payment gateway response
    """
    payment = get_object_or_404(
        Payment, 
        id=payment_id, 
        order__user=request.user,
        status='pending'
    )
    
    serializer = MockPaymentSerializer(data=request.data)
    
    if serializer.is_valid():
        success = serializer.validated_data['success']
        transaction_id = serializer.validated_data['transaction_id']
        
        if success:
            # Simulate successful payment
            payment.status = 'completed'
            payment.transaction_id = transaction_id
            
            # Update order status to confirmed
            payment.order.status = 'confirmed'
            payment.order.save()
        else:
            # Simulate failed payment
            payment.status = 'failed'
        
        payment.save()
        
        return Response({
            "message": "Payment processed successfully" if success else "Payment failed",
            "status": payment.status,
            "transaction_id": payment.transaction_id if success else None
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def request_refund(request, payment_id):
    """
    Request payment refund
    - User must be logged in
    - Can only request refund for their own payments
    - Payment must be completed and refundable
    """
    payment = get_object_or_404(
        Payment, 
        id=payment_id, 
        order__user=request.user
    )
    
    serializer = PaymentRefundSerializer(
        data=request.data,
        context={'payment': payment}
    )
    
    if serializer.is_valid():
        reason = serializer.validated_data['reason']
        refund_amount = serializer.validated_data.get('refund_amount', payment.amount)
        
        
        payment.status = 'refunded'
        payment.save()
        
        # Update order status to cancelled
        payment.order.status = 'cancelled'
        payment.order.save()
        
        return Response({
            "message": "Refund request submitted successfully",
            "refund_amount": refund_amount,
            "reason": reason
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminPaymentListView(generics.ListAPIView):
    """
    Get all payments (Admin only)
    - Admin users only
    - Shows all payments in the system
    """
    serializer_class = PaymentListSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Payment.objects.all().select_related('order', 'order__user').order_by('-created_at')


class AdminPaymentDetailView(generics.RetrieveAPIView):
    """
    Get payment details (Admin only)
    - Admin users only
    - Can view any payment
    """
    serializer_class = PaymentDetailSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Payment.objects.all()


class AdminPaymentStatusView(generics.UpdateAPIView):
    """
    Update payment status (Admin only)
    - Admin users only
    - Can update any payment status
    - Used for manual status updates or webhook handling
    """
    serializer_class = PaymentStatusSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Payment.objects.all()
    
    def perform_update(self, serializer):
        payment = serializer.save()
        
        # Update order status based on payment status
        if payment.status == 'completed':
            payment.order.status = 'confirmed'
            payment.order.save()
        elif payment.status in ['failed', 'cancelled']:
            payment.order.status = 'pending'
            payment.order.save()
        elif payment.status == 'refunded':
            payment.order.status = 'cancelled'
            payment.order.save()


@api_view(['POST'])
@permission_classes([permissions.AllowAny])  
def payment_webhook(request, provider):
    """
    Handle payment webhooks from payment providers
    - Public access (called by payment providers)
    - Verify webhook signature for security
    - Update payment status based on provider response
    """
    
    
    return Response({"status": "Webhook received"}, status=status.HTTP_200_OK)