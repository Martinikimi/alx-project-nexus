from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # User endpoints
    path('my/', views.UserPaymentsListView.as_view(), name='my-payments'),
    path('<int:pk>/', views.PaymentDetailView.as_view(), name='payment-detail'),
    path('create/', views.CreatePaymentView.as_view(), name='create-payment'),
    path('<int:payment_id>/process-mock/', views.process_mock_payment, name='process-mock-payment'),
    path('<int:payment_id>/request-refund/', views.request_refund, name='request-refund'),
    
    # Admin endpoints
    path('admin/all/', views.AdminPaymentListView.as_view(), name='admin-all-payments'),
    path('admin/<int:pk>/', views.AdminPaymentDetailView.as_view(), name='admin-payment-detail'),
    path('admin/<int:pk>/status/', views.AdminPaymentStatusView.as_view(), name='admin-payment-status'),
    
    # Webhook endpoints (called by payment providers)
    path('webhook/stripe/', views.payment_webhook, name='stripe-webhook'),
    path('webhook/mpesa/', views.payment_webhook, name='mpesa-webhook'),
    path('webhook/paypal/', views.payment_webhook, name='paypal-webhook'),
]