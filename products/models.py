from django.db import models
from categories.models import Category
import random
import hashlib

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    category = models.ForeignKey(Category, on_delete=models.CASCADE) 
    stock_quantity = models.IntegerField(default=0)
    sku = models.CharField(max_length=50, unique=True, blank=True) 
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

    def generate_sku(self):
        """
        Auto-generate SKU from category name, product name, and brand
        Format: CAT-BR-NAME-UNIQUE
        Example: ELE-AP-IPHO-A1B2
        """
        # AUTO category code from category name
        if self.category and self.category.name:
            category_name = self.category.name.upper().replace(' ', '')
            cat_code = category_name[:3] if len(category_name) >= 3 else category_name.ljust(3, 'X')[:3]
        else:
            cat_code = "GEN"
        
        # Clean product name (remove special chars, take first 4 chars)
        clean_name = ''.join([c for c in self.name if c.isalnum()])
        name_code = clean_name[:4].upper() if clean_name else "PROD"
        
        
        brand_code = "PR"
        
        # Unique hash to ensure uniqueness
        unique_hash = hashlib.md5(f"{self.name}{random.random()}".encode()).hexdigest()[:4].upper()
        
        return f"{cat_code}-{brand_code}-{name_code}-{unique_hash}"
    
    def save(self, *args, **kwargs):
        """
        Auto-generate SKU before saving if not provided
        """
        if not self.sku:
            self.sku = self.generate_sku()
            while Product.objects.filter(sku=self.sku).exists():
                self.sku = self.generate_sku()
        super().save(*args, **kwargs)