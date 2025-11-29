from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_order_email_to_admin(order):
    """Send email to admin when a new order is placed"""
    try:
        subject = f"🛒 New Order Received - #{order.order_number}"
        
        # Get order items
        items = order.items.all()
        
        # Create context for the template
        context = {
            'order': order,
            'items': items,
            'settings': settings
        }
        
        html_content = render_to_string('emails/admin_order_notification.html', context)
        text_content = strip_tags(html_content)
        
        email = EmailMultiAlternatives(
            subject,
            text_content,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        
        logger.info(f"Admin notification sent for order #{order.order_number}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send admin email for order #{order.order_number}: {e}")
        return False

def send_order_confirmation_to_customer(order):
    """Send order confirmation email to customer"""
    try:
        customer_email = order.user.email
        
        subject = f"✅ Order Confirmation - #{order.order_number}"
        
        # Get order items
        items = order.items.all()
        
        # Create context for the template
        context = {
            'order': order,
            'items': items,
            'customer_name': order.user.get_full_name() or order.user.username,
            'settings': settings
        }
        
        html_content = render_to_string('emails/customer_order_confirmation.html', context)
        text_content = strip_tags(html_content)
        
        email = EmailMultiAlternatives(
            subject,
            text_content,
            settings.DEFAULT_FROM_EMAIL,
            [customer_email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        
        logger.info(f"Order confirmation sent to {customer_email} for order #{order.order_number}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send customer email for order #{order.order_number}: {e}")
        return False

def send_order_notifications(order):
    """Send both admin and customer notifications"""
    admin_sent = send_order_email_to_admin(order)
    customer_sent = send_order_confirmation_to_customer(order)
    
    return {
        'admin_notification_sent': admin_sent,
        'customer_notification_sent': customer_sent
    }