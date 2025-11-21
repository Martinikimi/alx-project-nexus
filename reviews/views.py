from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Count, Q
from .models import Review
from .serializers import (ReviewListSerializer,ReviewDetailSerializer,ReviewCreateSerializer,ReviewUpdateSerializer,
ReviewHelpfulSerializer,
ProductReviewStatsSerializer
)
from products.models import Product

class ProductReviewsListView(generics.ListAPIView):
    """
    Get all reviews for a specific product
    - Public access (no login required)
    - Shows verified purchase badges
    """
    serializer_class = ReviewListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return Review.objects.filter(
            product_id=product_id
        ).select_related('user', 'product').order_by('-created_at')


class UserReviewsListView(generics.ListAPIView):
    """
    Get user's review history
    - User must be logged in
    - Shows user's own reviews
    """
    serializer_class = ReviewListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(
            user=self.request.user
        ).select_related('product').order_by('-created_at')


class ReviewDetailView(generics.RetrieveAPIView):
    """
    Get review details
    - Public access (no login required)
    """
    serializer_class = ReviewDetailSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Review.objects.all().select_related('user', 'product')


class CreateReviewView(generics.CreateAPIView):
    """
    Create new review
    - User must be logged in
    - Must have purchased the product
    - One review per product per user
    """
    serializer_class = ReviewCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UpdateReviewView(generics.UpdateAPIView):
    """
    Update user's own review
    - User must be logged in
    - Can only update own reviews
    """
    serializer_class = ReviewUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users can only update their own reviews
        return Review.objects.filter(user=self.request.user)


class DeleteReviewView(generics.DestroyAPIView):
    """
    Delete user's own review
    - User must be logged in
    - Can only delete own reviews
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users can only delete their own reviews
        return Review.objects.filter(user=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_review_helpful(request, review_id):
    """
    Mark review as helpful
    - User must be logged in
    - Can't vote on own reviews
    - Can't vote multiple times
    """
    review = get_object_or_404(Review, id=review_id)
    
    # Can't vote on own review
    if review.user == request.user:
        return Response(
            {"error": "You cannot vote on your own review."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    serializer = ReviewHelpfulSerializer(
        data=request.data,
        context={'request': request, 'review': review}
    )
    
    if serializer.is_valid():
        helpful = serializer.validated_data['helpful']
        
        if helpful:
            # Add user to helpful votes
            review.helpful_votes.add(request.user)
            review.helpful_count = review.helpful_votes.count()
            review.save()
        else:
            # Remove user from helpful votes
            review.helpful_votes.remove(request.user)
            review.helpful_count = review.helpful_votes.count()
            review.save()
        
        return Response(
            {"message": "Vote recorded successfully", "helpful_count": review.helpful_count}
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def product_review_stats(request, product_id):
    """
    Get review statistics for a product
    - Public access (no login required)
    - Average rating, total reviews, rating breakdown
    """
    product = get_object_or_404(Product, id=product_id)
    
    # Calculate statistics
    reviews = Review.objects.filter(product=product)
    total_reviews = reviews.count()
    
    if total_reviews > 0:
        average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        
        # Rating breakdown (1-5 stars)
        rating_breakdown = {}
        for rating in range(1, 6):
            count = reviews.filter(rating=rating).count()
            rating_breakdown[str(rating)] = count
        
        verified_reviews_count = reviews.filter(verified_purchase=True).count()
    else:
        average_rating = 0
        rating_breakdown = {str(i): 0 for i in range(1, 6)}
        verified_reviews_count = 0
    
    stats = {
        'average_rating': round(average_rating, 1) if average_rating else 0,
        'total_reviews': total_reviews,
        'rating_breakdown': rating_breakdown,
        'verified_reviews_count': verified_reviews_count
    }
    
    serializer = ProductReviewStatsSerializer(stats)
    return Response(serializer.data)


class AdminReviewListView(generics.ListAPIView):
    """
    Get all reviews (Admin only)
    - Admin users only
    - Shows all reviews in the system
    """
    serializer_class = ReviewDetailSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Review.objects.all().select_related('user', 'product').order_by('-created_at')