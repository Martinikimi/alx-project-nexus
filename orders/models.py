from django.db import models
from django.conf import settings
from django.utils import timezone
from products.models import Product 
from users.models import User

class Order(models.Model):
    # Order status
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

    class Meta:
        app_label = 'orders'

    def __str__(self):
        return f"Order {self.order_number} by {self.user.email}"

    @classmethod
    def create_from_cart(cls, cart, shipping_address):
        # Generate unique order number
        order_number = f"ORD-{timezone.now().strftime('%Y%m%d%H%M%S')}"
        
        # Create the order first with temporary total
        order = cls.objects.create(
            user=cart.user,
            order_number=order_number,
            shipping_address=shipping_address,
            total_amount=0,  
            status='pending'
        )
        
        
        total = 0
        for cart_item in cart.items.all():
            # Create OrderItem for each CartItem
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price 
            )
            total += cart_item.product.price * cart_item.quantity
        
        # Update order total with actual calculated amount
        order.total_amount = total
        order.save()
        
        # Clear cart after successful order creation
        cart.items.all().delete()
        
        return order

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        app_label = 'orders'

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.order_number}"