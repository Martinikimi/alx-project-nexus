from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    # Public endpoints
    path('product/<int:product_id>/', views.ProductReviewsListView.as_view(), name='product-reviews'),
    path('product/<int:product_id>/stats/', views.product_review_stats, name='product-review-stats'),
    path('<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),
    
    # User endpoints (require authentication)
    path('my/', views.UserReviewsListView.as_view(), name='my-reviews'),
    path('create/', views.CreateReviewView.as_view(), name='create-review'),
    path('<int:pk>/update/', views.UpdateReviewView.as_view(), name='update-review'),
    path('<int:pk>/delete/', views.DeleteReviewView.as_view(), name='delete-review'),
    path('<int:review_id>/helpful/', views.mark_review_helpful, name='mark-helpful'),
    
    # Admin endpoints
    path('admin/all/', views.AdminReviewListView.as_view(), name='admin-all-reviews'),
]