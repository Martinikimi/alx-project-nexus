from django.db import models
from django.conf import settings
from products.models import Product
from users.models import User

class Cart(models.Model):
    # Each user gets ONE shopping cart
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user.email}"

    # Total price of all items in cart
    @property
    def total_price(self):
        total = 0
        for item in self.items.all():
            total += item.product.price * item.quantity
        return total

    # Total items in cart
    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

class CartItem(models.Model):
    # Each product added to cart becomes a CartItem
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # How many of this product
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['cart', 'product']

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    # Calculate price for this specific item
    @property
    def item_price(self):
        return self.product.price * self.quantity