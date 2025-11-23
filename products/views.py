from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Product
from .serializers import (ProductListSerializer,ProductDetailSerializer,ProductCreateSerializer)
from categories.models import Category
from rest_framework.response import Response


class ProductSearchView(generics.ListAPIView):
    """
    Enhanced product search with helpful 'no results' messages
    - Public access (no login required)
    - Searches in product names and descriptions
    - Optional price range filtering
    - Optional category filtering
    - Optional sorting
    - Helpful messages when no results found
    - Pagination support (15 products per page default)
    """
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    
    def list(self, request, *args, **kwargs):
        """
        Override the list method to add custom messages when no results found
        Now includes pagination support
        """
        # Get pagination parameters - using 15 as default choice
        page_size = int(request.query_params.get('page_size', 15))
        page = int(request.query_params.get('page', 1))
        
        # reasonable limits
        page_size = min(page_size, 48)  # max 48 products per page
        page_size = max(page_size, 4)   # min 4 products per page
        page = max(page, 1)             # min page 1
        
        # Get the base queryset
        queryset = self.get_queryset()
        
        # Calculate pagination numbers
        total_products = queryset.count()
        total_pages = (total_products + page_size - 1) // page_size  
        start_index = (page - 1) * page_size
        end_index = min(start_index + page_size, total_products)
        
        # Get just the products for this page
        paginated_products = queryset[start_index:end_index]
        
        # Serialize the paginated products
        serializer = self.get_serializer(paginated_products, many=True)
        
        # Build our custom response with pagination
        response_data = {
            'products': serializer.data,
            'pagination': {
                'current_page': page,
                'page_size': page_size,
                'total_products': total_products,
                'total_pages': total_pages,
                'has_next': page < total_pages,
                'has_previous': page > 1,
                'next_page': page + 1 if page < total_pages else None,
                'previous_page': page - 1 if page > 1 else None,
            }
        }
        
        # Get search query for custom messages
        search_query = self.request.query_params.get('q', '').strip()
        has_other_filters = any([
            self.request.query_params.get('min_price'),
            self.request.query_params.get('max_price'), 
            self.request.query_params.get('category'),
            self.request.query_params.get('sort')
        ])
        
        # Custom message if no results found
        if len(response_data['products']) == 0:
            if search_query:
                response_data['message'] = f'There are no results for "{search_query}".'
                response_data['suggestions'] = [
                    'Check your spelling for typing errors',
                    'Try searching with short and simple keywords'
                ]
                response_data['search_performed'] = True
                response_data['results_count'] = 0
            elif has_other_filters:
                response_data['message'] = 'No products match your filters.'
                response_data['suggestions'] = [
                    'Try adjusting your price range',
                    'Try a different category',
                    'Remove some filters to see more products'
                ]
                response_data['search_performed'] = True
                response_data['results_count'] = 0
            else:
                # No search and no filters 
                response_data['search_performed'] = False
                response_data['results_count'] = 0
        else:
            # Results found 
            response_data['search_performed'] = bool(search_query or has_other_filters)
            response_data['results_count'] = len(response_data['products'])
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


class ProductListView(generics.ListAPIView):
    """
    Enhanced product list with search, filtering, and sorting
    - Public access (no login required)
    - Only shows active products
    - Supports search, price filtering, category filtering, and sorting
    - Now with pagination (15 products per page default)
    - Examples:
    /api/products/                           
    /api/products/?q=shoes                   
    /api/products/?min_price=50&max_price=100 
    /api/products/?category=3                
    /api/products/?sort=price_asc            
    /api/products/?q=phone&sort=rating_desc  
    /api/products/?page=2&page_size=20      
    """
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        """
        Override list method to add pagination
        """
        # Get pagination parameters - 15 as default
        page_size = int(request.query_params.get('page_size', 15))
        page = int(request.query_params.get('page', 1))
        
        # reasonable limits
        page_size = min(page_size, 48)  # max 48 products per page
        page_size = max(page_size, 4)   # min 4 products per page
        page = max(page, 1)             # min page 1
        
        # Get the base queryset
        queryset = self.get_queryset()
        
        # Calculate pagination numbers
        total_products = queryset.count()
        total_pages = (total_products + page_size - 1) // page_size  
        start_index = (page - 1) * page_size
        end_index = min(start_index + page_size, total_products)
        
        # Get just the products for this page
        paginated_products = queryset[start_index:end_index]
        
        # Serialize the paginated products
        serializer = self.get_serializer(paginated_products, many=True)
        
        # Build paginated response
        response_data = {
            'products': serializer.data,
            'pagination': {
                'current_page': page,
                'page_size': page_size,
                'total_products': total_products,
                'total_pages': total_pages,
                'has_next': page < total_pages,
                'has_previous': page > 1,
                'next_page': page + 1 if page < total_pages else None,
                'previous_page': page - 1 if page > 1 else None,
            },
            'filters_applied': {
                'search': bool(request.query_params.get('q')),
                'category': bool(request.query_params.get('category')),
                'price_range': bool(request.query_params.get('min_price') or request.query_params.get('max_price')),
                'sorting': bool(request.query_params.get('sort')),
            }
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
            'date_desc': '-created_at',     # Newest first
            'date_asc': 'created_at',       # Oldest first
            'name_asc': 'name',             # Name A-Z
            'name_desc': '-name',           # Name Z-A
        }
        
        if sort_option in sort_mappings:
            return queryset.order_by(sort_mappings[sort_option])
        
        # Default sorting (newest first)
        return queryset.order_by('-created_at')


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
