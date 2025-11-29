from rest_framework import generics, permissions
from django.db.models import Q
from .models import Product
from .serializers import (ProductListSerializer, ProductDetailSerializer, ProductCreateSerializer)
from categories.models import Category
from rest_framework.response import Response
from rest_framework.decorators import api_view


class ProductPagination:
    """
    Custom pagination class to match frontend expectations
    """
    def __init__(self):
        self.page_size = 15
        self.page_size_query_param = 'page_size'
        self.max_page_size = 100

    def paginate_queryset(self, queryset, request, view=None):
        # Get pagination parameters
        try:
            self.page_size = int(request.query_params.get('page_size', 15))
        except (ValueError, TypeError):
            self.page_size = 15
            
        try:
            self.page_number = int(request.query_params.get('page', 1))
        except (ValueError, TypeError):
            self.page_number = 1

        # Apply reasonable limits
        self.page_size = min(self.page_size, 100)
        self.page_size = max(self.page_size, 1)
        self.page_number = max(self.page_number, 1)

        # Calculate pagination
        self.total_count = queryset.count()
        self.total_pages = (self.total_count + self.page_size - 1) // self.page_size
        start_index = (self.page_number - 1) * self.page_size
        end_index = min(start_index + self.page_size, self.total_count)
        
        # Return paginated queryset
        return list(queryset[start_index:end_index])

    def get_paginated_response(self, data):
        return {
            'results': data,
            'current_page': self.page_number,
            'total_pages': self.total_pages,
            'total_count': self.total_count,
            'page_size': self.page_size,
            'has_next': self.page_number < self.total_pages,
            'has_previous': self.page_number > 1,
        }


@api_view(['GET'])
def debug_test(request):
    """Debug endpoint to find the exact error"""
    try:
        # Test 1: Can we import the model?
        from .models import Product
        print("✓ Model imported successfully")
        
        # Test 2: Can we query the database?
        count = Product.objects.count()
        print(f"✓ Database query successful - {count} products")
        
        # Test 3: Can we import serializers?
        from .serializers import ProductListSerializer
        print("✓ Serializers imported successfully")
        
        # Test 4: Try to serialize
        products = Product.objects.all()[:1]
        if products:
            serializer = ProductListSerializer(products, many=True, context={'request': request})
            data = serializer.data
            print("✓ Serialization successful")
        
        return Response({
            "status": "success",
            "message": "All tests passed",
            "product_count": count
        })
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        
        return Response({
            "status": "error", 
            "message": str(e),
            "error_type": type(e).__name__,
        }, status=500)


class ProductListView(generics.ListAPIView):
    """
    Enhanced product list with search, filtering, and sorting
    - Public access (no login required)
    - Only shows active products
    - Supports search, price filtering, category filtering, and sorting
    - Now with pagination that matches frontend expectations
    """
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_context(self):
        return {'request': self.request}

    def list(self, request, *args, **kwargs):
        """
        Override list method to use custom pagination format
        """
        # Get the base queryset
        queryset = self.get_queryset()
        
        # Apply custom pagination
        paginator = ProductPagination()
        paginated_products = paginator.paginate_queryset(queryset, request)
        
        # Serialize the paginated products
        serializer = self.get_serializer(paginated_products, many=True)
        
        # Build response with frontend-compatible format
        response_data = paginator.get_paginated_response(serializer.data)
        
        # Add additional info for frontend
        response_data['filters_applied'] = {
            'search': bool(request.query_params.get('q')),
            'category': bool(request.query_params.get('category')),
            'price_range': bool(request.query_params.get('min_price') or request.query_params.get('max_price')),
            'sorting': bool(request.query_params.get('sort')),
        }
        
        return Response(response_data)

    def get_queryset(self):
        # Get search, filter, and sort parameters from URL
        search_query = self.request.query_params.get('q', '')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        category_id = self.request.query_params.get('category')
        sort_option = self.request.query_params.get('sort', '')
        
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
        
        # Apply sorting
        queryset = self.apply_sorting(queryset, sort_option)
        
        return queryset.select_related('category')
    
    def apply_sorting(self, queryset, sort_option):
        """
        Apply sorting based on the sort parameter
        """
        sort_mappings = {
            'price_asc': 'price',           # Price low to high
            'price_desc': '-price',         # Price high to low
            'date_asc': 'created_at',       # Oldest first
            'date_desc': '-created_at',     # Newest first (default)
            'name_asc': 'name',             # Name A-Z
            'name_desc': '-name',           # Name Z-A
        }
        
        if sort_option in sort_mappings:
            return queryset.order_by(sort_mappings[sort_option])
        
        # Default sorting (newest first)
        return queryset.order_by('-created_at')


class ProductSearchView(generics.ListAPIView):
    """
    Enhanced product search with helpful 'no results' messages
    - Uses the same format as ProductListView for consistency
    """
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    def list(self, request, *args, **kwargs):
        """
        Override the list method to use consistent pagination format
        """
        # Get the base queryset
        queryset = self.get_queryset()
        
        # Apply custom pagination
        paginator = ProductPagination()
        paginated_products = paginator.paginate_queryset(queryset, request)
        
        # Serialize the paginated products
        serializer = self.get_serializer(paginated_products, many=True)
        
        # Build response with frontend-compatible format
        response_data = paginator.get_paginated_response(serializer.data)
        
        # Get search query for custom messages
        search_query = self.request.query_params.get('q', '').strip()
        has_other_filters = any([
            self.request.query_params.get('min_price'),
            self.request.query_params.get('max_price'), 
            self.request.query_params.get('category'),
            self.request.query_params.get('sort')
        ])
        
        # Custom message if no results found
        if len(response_data['results']) == 0:
            if search_query:
                response_data['message'] = f'There are no results for "{search_query}".'
                response_data['suggestions'] = [
                    'Check your spelling for typing errors',
                    'Try searching with short and simple keywords'
                ]
                response_data['search_performed'] = True
            elif has_other_filters:
                response_data['message'] = 'No products match your filters.'
                response_data['suggestions'] = [
                    'Try adjusting your price range',
                    'Try a different category',
                    'Remove some filters to see more products'
                ]
                response_data['search_performed'] = True
            else:
                # No search and no filters 
                response_data['search_performed'] = False
        else:
            # Results found 
            response_data['search_performed'] = bool(search_query or has_other_filters)
            if search_query:
                response_data['search_query'] = search_query
        
        return Response(response_data)
    
    def get_queryset(self):
        # Search parameters from URL
        search_query = self.request.query_params.get('q', '')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        category_id = self.request.query_params.get('category')
        sort_option = self.request.query_params.get('sort', '')
        
        # Start with active products
        queryset = Product.objects.filter(is_active=True)
        
        # Apply search filter if provided
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
        
        # minimum price filter
        if min_price:
            try:
                min_price = float(min_price)
                queryset = queryset.filter(price__gte=min_price)
            except (ValueError, TypeError):
                pass
        
        # maximum price filter
        if max_price:
            try:
                max_price = float(max_price)
                queryset = queryset.filter(price__lte=max_price)
            except (ValueError, TypeError):
                pass
        
        # category filter
        if category_id:
            try:
                category_id = int(category_id)
                queryset = queryset.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass
        
        # sorting
        queryset = self.apply_sorting(queryset, sort_option)
        
        return queryset.select_related('category')
    
    def apply_sorting(self, queryset, sort_option):
        """
        Apply sorting based on the sort parameter
        """
        sort_mappings = {
            'price_asc': 'price',           # Price low to high
            'price_desc': '-price',         # Price high to low
            'date_desc': '-created_at',     # Newest first
            'date_asc': 'created_at',       # Oldest first
            'name_asc': 'name',             # Name A-Z
            'name_desc': '-name',           # Name Z-A
        }
        
        if sort_option in sort_mappings:
            return queryset.order_by(sort_mappings[sort_option])
        
        # Default sorting 
        return queryset.order_by('-created_at')


class ProductDetailView(generics.RetrieveAPIView):
    """
    Get single product details
    - Public access (no login required)
    - Shows full product information
    """
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        # Return active products only
        return Product.objects.filter(is_active=True).select_related('category')


class CategoryProductsView(generics.ListAPIView):
    """
    Get products by category
    - Public access
    - Shows products from specific category and its subcategories
    - Uses same pagination format as ProductListView
    """
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_context(self):
        return {'request': self.request}

    def list(self, request, *args, **kwargs):
        """
        Override list method to use consistent pagination
        """
        # Get the base queryset
        queryset = self.get_queryset()
        
        # Apply custom pagination
        paginator = ProductPagination()
        paginated_products = paginator.paginate_queryset(queryset, request)
        
        # Serialize the paginated products
        serializer = self.get_serializer(paginated_products, many=True)
        
        # Build response with frontend-compatible format
        response_data = paginator.get_paginated_response(serializer.data)
        
        return Response(response_data)

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


class FeaturedProductsView(generics.ListAPIView):
    """
    Get featured products only
    - Public access
    - Returns simple array (no pagination) for featured products
    """
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        return Product.objects.filter(
            is_featured=True,
            is_active=True
        ).select_related('category').order_by('-created_at')[:8] 

    def list(self, request, *args, **kwargs):
        """
        Return simple array for featured products (no pagination needed)
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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