from rest_framework import serializers
from .models import Category

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'is_active']


class CategoryDetailSerializer(serializers.ModelSerializer):
    subcategories = CategoryListSerializer(many=True, read_only=True)
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'parent', 'parent_name', 'slug', 'is_active', 'subcategories', 'created_at', 'updated_at']


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'description', 'parent', 'is_active']