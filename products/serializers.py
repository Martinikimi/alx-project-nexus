from rest_framework import serializers
from .models import Product
from categories.serializers import CategoryListSerializer

class ProductListSerializer(serializers.ModelSerializer):
    """Serializer for product listings """
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'category','category_name','is_featured', 'is_active']


class ProductDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for individual product pages"""
    category = CategoryListSerializer(read_only=True)
    
    class Meta:
        model = Product
        fields = [ 'id','name', 'description','price','category','stock_quantity','is_featured', 'is_active','created_at'
        ]


class ProductCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating products (admin only)"""
    class Meta:
        model = Product
        fields = ['name','description', 'price','category','stock_quantity','is_featured', 'is_active'
        ]