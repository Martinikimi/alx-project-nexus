from rest_framework import serializers
from .models import Review
from products.models import Product
from orders.models import Order

class ReviewListSerializer(serializers.ModelSerializer):
    """Serializer for listing reviews (public access)"""
    user_name = serializers.CharField(source='user.username', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'rating', 'comment', 'user_name', 'product_name',
            'verified_purchase', 'created_at', 'helpful_count'
        ]
        read_only_fields = ['verified_purchase', 'helpful_count']


class ReviewDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed review view"""
    user_name = serializers.CharField(source='user.username', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'rating', 'comment', 'user_name', 'user_email', 
            'product_name', 'verified_purchase', 'created_at', 'updated_at',
            'helpful_count'
        ]
        read_only_fields = [
            'user_name', 'user_email', 'verified_purchase', 
            'helpful_count', 'created_at', 'updated_at'
        ]


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating reviews with purchase verification"""
    product_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Review
        fields = ['product_id', 'rating', 'comment']
    
    def validate_product_id(self, value):
        """Validate that product exists"""
        try:
            product = Product.objects.get(id=value, is_active=True)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found.")
        return value
    
    def validate_rating(self, value):
        """Validate rating is between 1-5"""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5 stars.")
        return value
    
    def validate(self, data):
        """Validate that user has purchased the product"""
        user = self.context['request'].user
        product_id = data['product_id']
        
        # Check if user has purchased this product (delivered orders only)
        has_purchased = Order.objects.filter(
            user=user,
            items__product_id=product_id,
            status='delivered'
        ).exists()
        
        if not has_purchased:
            raise serializers.ValidationError(
                "You can only review products you have purchased and received."
            )
        
        # Check if user already reviewed this product
        if Review.objects.filter(user=user, product_id=product_id).exists():
            raise serializers.ValidationError(
                "You have already reviewed this product."
            )
        
        return data
    
    def create(self, validated_data):
        """Create review with verified purchase flag"""
        product_id = validated_data.pop('product_id')
        product = Product.objects.get(id=product_id)
        
        review = Review.objects.create(
            user=self.context['request'].user,
            product=product,
            rating=validated_data['rating'],
            comment=validated_data['comment'],
            verified_purchase=True 
        )
        
        return review


class ReviewUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating reviews"""
    class Meta:
        model = Review
        fields = ['rating', 'comment']
    
    def validate_rating(self, value):
        """Validate rating is between 1-5"""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5 stars.")
        return value


class ReviewHelpfulSerializer(serializers.Serializer):
    """Serializer for marking review as helpful"""
    helpful = serializers.BooleanField(default=True)
    
    def validate(self, data):
        """Validate user hasn't already voted"""
        user = self.context['request'].user
        review = self.context['review']
        
        if review.helpful_votes.filter(id=user.id).exists():
            raise serializers.ValidationError("You have already voted on this review.")
        
        return data


class ProductReviewStatsSerializer(serializers.Serializer):
    """Serializer for product review statistics"""
    average_rating = serializers.FloatField()
    total_reviews = serializers.IntegerField()
    rating_breakdown = serializers.DictField()
    verified_reviews_count = serializers.IntegerField()