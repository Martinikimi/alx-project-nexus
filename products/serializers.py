from rest_framework import serializers
from .models import Product
from categories.serializers import CategoryListSerializer

class ProductListSerializer(serializers.ModelSerializer):
    """Serializer for product listings """
    category_name = serializers.CharField(source='category.name', read_only=True)
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'category', 'category_name', 'image', 'is_featured', 'is_active']
    
    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            else:
                # Fallback for production - use your actual Render URL
                return f"https://alx-project-nexus-agn5.onrender.com/media/{obj.image.url}"
        return None


class ProductDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for individual product pages"""
    category = CategoryListSerializer(read_only=True)
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'stock_quantity', 'image', 'is_featured', 'is_active', 'created_at']
    
    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            else:
                # Fallback for production - use your actual Render URL
                return f"https://alx-project-nexus-agn5.onrender.com/media/{obj.image.url}"
        return None


class ProductCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating products (admin only)"""
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'stock_quantity', 'image', 'is_featured', 'is_active']