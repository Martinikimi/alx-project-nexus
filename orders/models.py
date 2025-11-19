from django.db import models
from django.conf import settings
from products.models import Product 
from users.models import User

class Order(models.Model):
    # Order status like package tracking
    STATUS_CHOICES = [
        ('pending', 'Pending'),      
        ('confirmed', 'Confirmed'),  
        ('shipped', 'Shipped'),      
        ('delivered', 'Delivered'),  
        ('cancelled', 'Cancelled'),  
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=20, unique=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Order {self.order_number} by {self.user.email}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.order_number}"