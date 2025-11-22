from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from products.models import Product
from users.models import User

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    verified_purchase = models.BooleanField(default=False)
    comment = models.TextField()
    helpful_count = models.PositiveIntegerField(default=0)
    
    # Rating: 1-5 stars ⭐⭐⭐⭐☆
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    
    # Admin can approve/disapprove reviews
    is_approved = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'product']

    def __str__(self):
        return f"{self.user.email} - {self.product.name} - {self.rating} stars"

    # Display stars
    @property
    def stars(self):
        return '⭐' * self.rating + '☆' * (5 - self.rating)