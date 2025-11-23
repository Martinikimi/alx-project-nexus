from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Product
from .serializers import (ProductListSerializer,ProductDetailSerializer,ProductCreateSerializer)
from categories.models import Category


class ProductSearchView(generics.ListAPIView):
    """
    Enhanced product search with helpful 'no results' messages
    - Public access (no login required)
    - Searches in product names and descriptions
    - Optional price range filtering
    - Optional category filtering
    - Helpful messages when no results found
    """
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    
    def list(self, request, *args, **kwargs):
        """
        Override the list method to add custom messages when no results found
        """
        # Get the original response
        response = super().list(request, *args, **kwargs)
        
        # Get search query for our custom message
        search_query = self.request.query_params.get('q', '').strip()
        has_other_filters = any([
            self.request.query_params.get('min_price'),
            self.request.query_params.get('max_price'), 
            self.request.query_params.get('category')
        ])
        
        # Add custom message if no results found
        if len(response.data) == 0:
            if search_query:
                response.data = {
                    'message': f'There are no results for "{search_query}".',
                    'suggestions': [
                        'Check your spelling for typing errors',
                        'Try searching with short and simple keywords'
                    ],
                    'search_performed': True,
                    'results_count': 0,
                    'products': []
                }
            elif has_other_filters:
                response.data = {
                    'message': 'No products match your filters.',
                    'suggestions': [
                        'Try adjusting your price range',
                        'Try a different category',
                        'Remove some filters to see more products'
                    ],
                    'search_performed': True,
                    'results_count': 0,
                    'products': []
                }
            else:
                # No search and no filters - just empty products
                response.data = {
                    'search_performed': False,
                    'results_count': 0,
                    'products': []
                }
        else:
            # Results found - add metadata
            response.data = {
                'search_performed': bool(search_query or has_other_filters),
                'results_count': len(response.data),
                'products': response.data
            }
            if search_query:
                response.data['search_query'] = search_query
        
        return response
    
    def get_queryset(self):
        # Get search parameters from URL
        search_query = self.request.query_params.get('q', '')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        category_id = self.request.query_params.get('category')
        
        # Start with all active products
        queryset = Product.objects.filter(is_active=True)
        
        # Apply search filter if provided
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
        
        # Apply minimum price filter
        if min_price:
            try:
                min_price = float(min_price)
                queryset = queryset.filter(price__gte=min_price)
            except (ValueError, TypeError):
                pass
        
        # Apply maximum price filter
        if max_price:
            try:
                max_price = float(max_price)
                queryset = queryset.filter(price__lte=max_price)
            except (ValueError, TypeError):
                pass
        
        # Apply category filter
        if category_id:
            try:
                category_id = int(category_id)
                queryset = queryset.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass
        
        return queryset.select_related('category')

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
