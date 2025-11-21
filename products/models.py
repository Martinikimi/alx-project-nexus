from django.db import models
from categories.models import Category

class Product(models.Model):
    name = models.CharField(max_length=15)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    category = models.ForeignKey(Category, on_delete=models.CASCADE) 
    stock_quantity = models.IntegerField(default=0)
    sku = models.CharField(max_length=50, unique=True)  
    image = models.ImageField(upload_to='products/', blank=True, null=True) 
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True) 


    def __str__(self):
        return self.name

    @property
    def in_stock(self):
        return self.stock_quantity > 0

    @property
    def low_stock(self):
        return 0 < self.stock_quantity <= 10