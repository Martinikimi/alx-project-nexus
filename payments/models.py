from django.db import models
from django.conf import settings
from orders.models import Order

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),      
        ('completed', 'Completed'),  
        ('failed', 'Failed'),        
        ('refunded', 'Refunded'),  
        ('cancelled', 'Cancelled'),  
    ]
    
    # Payment methods 
    METHOD_CHOICES = [
        ('mpesa', 'M-Pesa'),
        ('card', 'Credit/Debit Card'),
        ('paypal', 'PayPal'),
        ('bank', 'Bank Transfer'),
    ]
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    payment_method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.transaction_id} - {self.status}"

    # Check if payment was successful
    @property
    def is_successful(self):
        return self.status == 'completed'

    # Check if payment can be refunded
    @property
    def can_refund(self):
        return self.status == 'completed'