from rest_framework import serializers
from .models import Category

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'is_active']


class CategoryDetailSerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'parent', 'parent_name', 'slug', 'is_active', 'subcategories', 'created_at', 'updated_at']
    
    def get_subcategories(self, obj):
        # Get all active subcategories
        subcategories = Category.objects.filter(parent=obj, is_active=True)
        return CategoryListSerializer(subcategories, many=True).data


class CategoryAdminSerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'parent', 'parent_name', 'slug', 'is_active', 'subcategories', 'created_at', 'updated_at']
    
    def get_subcategories(self, obj):
        # Get ALL subcategories (including inactive) for admin
        subcategories = Category.objects.filter(parent=obj)
        return CategoryAdminSerializer(subcategories, many=True).data


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'description', 'parent', 'is_active']