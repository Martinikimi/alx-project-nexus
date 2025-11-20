from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db import models
from .models import Category
from .serializers import (CategoryListSerializer, CategoryDetailSerializer, CategoryCreateSerializer)


class CategoryListView(generics.ListAPIView):
    """
    List all categories
    - Public access with no authentication required
    - Only shows active categories
    """
    serializer_class = CategoryListSerializer
    permission_classes = [permissions.AllowAny] 
    
    def get_queryset(self):
        # Only active categories for non-admin users
        return Category.objects.filter(is_active=True)


class CategoryDetailView(generics.RetrieveAPIView):
    """
    Get  category details
    - Public access with no authentication required
    - Shows category with nested subcategories
    """
    serializer_class = CategoryDetailSerializer
    permission_classes = [permissions.AllowAny] 
    
    def get_queryset(self):
        # Only active categories for non-admin users
        return Category.objects.filter(is_active=True)


class CategoryCreateView(generics.CreateAPIView):
    """
    Create new category
    - Only admin users can create categories
    """
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer
    permission_classes = [permissions.IsAdminUser] 

    def perform_create(self, serializer):
        serializer.save()


class CategoryUpdateView(generics.UpdateAPIView):
    """
    Update existing category
    - Only admin users can update categories
    """
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer  
    permission_classes = [permissions.IsAdminUser] 


class CategoryDeleteView(generics.DestroyAPIView):
    """
    Delete category
    - Only admin users can delete categories
    """
    queryset = Category.objects.all()
    permission_classes = [permissions.IsAdminUser] 
    
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


# Admin-only view to see ALL categories including the inactive
class CategoryAdminListView(generics.ListAPIView):
    """
    List ALL categories (
    - Only admin users can access
    - Shows complete category list for management
    """
    serializer_class = CategoryListSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Category.objects.all()
    
