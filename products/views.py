from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Product
from .serializers import (ProductListSerializer,ProductDetailSerializer,ProductCreateSerializer)
from categories.models import Category


class ProductListView(generics.ListAPIView):
    """
    List all active products
    - Public access (no login required)
    - Only shows active products
    - Includes basic filtering
    """
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]


    def get_queryset(self):
        # Return active products only
        return Product.objects.filter(is_active=True).select_related('category')


class ProductDetailView(generics.RetrieveAPIView):
    """
    Get single product details
    - Public access (no login required)
    - Shows full product information
    """
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        # Return active products only
        return Product.objects.filter(is_active=True).select_related('category')


class CategoryProductsView(generics.ListAPIView):
    """
    Get products by category
    - Public access
    - Shows products from specific category and its subcategories
    """
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        
        # Get the category and all its subcategories
        try:
            category = Category.objects.get(id=category_id)
            descendant_categories = category.get_descendants(include_self=True)
            
            # Return products from this category and all subcategories
            return Product.objects.filter(
                category__in=descendant_categories,
                is_active=True
            ).select_related('category')
        except Category.DoesNotExist:
            return Product.objects.none()


class ProductCreateView(generics.CreateAPIView):
    """
    Create new product
    - Admin users only
    """
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = [permissions.IsAdminUser]


class ProductUpdateView(generics.UpdateAPIView):
    """
    Update existing product
    - Admin users only
    """
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = [permissions.IsAdminUser]


class ProductDeleteView(generics.DestroyAPIView):
    """
    Delete product (soft delete)
    - Admin users only
    - Sets is_active=False instead of actual deletion
    """
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

class FeaturedProductsView(generics.ListAPIView):
    """
    Get featured products only
    - Public access
    """
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Product.objects.filter(
            is_featured=True,
            is_active=True
        ).select_related('category')
