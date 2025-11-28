from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_order_confirmation(order):
    """
    Send order confirmation email to customer who placed the order
    """
    try:
        subject = f"Order Confirmation - #{order.order_number}"
        
        # Create HTML content
        html_content = render_to_string(
            'emails/order_confirmation.html',
            {
                'order': order,
                'order_items': order.items.all(),
                'store_name': 'NexusStore',
                'support_email': 'martinikimi7@gmail.com'
            }
        )
        
        text_content = strip_tags(html_content)
        
        # Create email - sends to CUSTOMER
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email='martinikimi7@gmail.com',  # my Gmail as sender
            to=[order.user.email],  # Customer's email
            reply_to=['martinikimi7@gmail.com']  # my email for replies
        )
        
        email.attach_alternative(html_content, "text/html")
        email.send()
        
        print(f"✅ REAL EMAIL: Order confirmation sent to CUSTOMER: {order.user.email}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send order confirmation: {e}")
        return False

def send_new_order_notification(order):
    """
    Send new order notification to ADMIN (you)
    """
    try:
        subject = f"🛍️ New Order Received - #{order.order_number}"
        
        # Create HTML content
        html_content = render_to_string(
            'emails/new_order_notification.html',
            {
                'order': order,
                'order_items': order.items.all(),
                'store_name': 'NexusStore'
            }
        )
        
        # Create plain text version
        text_content = strip_tags(html_content)
        
        # Create email - sends to ADMIN
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email='martinikimi7@gmail.com', 
            to=['martinikimi7@gmail.com'],  
            reply_to=[order.user.email]  
        )
        
        email.attach_alternative(html_content, "text/html")
        email.send()
        
        print(f"✅ REAL EMAIL: New order notification sent to ADMIN: martinikimi7@gmail.com")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send new order notification: {e}")
        return False
    
def send_order_status_update(order):
    """
    Send email to customer when order status changes
    """
    try:
        subject = f"Order Update - #{order.order_number} is now {order.status.title()}"
        
        # Create HTML content
        html_content = render_to_string(
            'emails/order_status_update.html',
            {
                'order': order,
                'order_items': order.items.all(),
                'store_name': 'NexusStore',
                'support_email': 'martinikimi7@gmail.com'
            }
        )
        
        # Create plain text version
        text_content = strip_tags(html_content)
        
        # Create email
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email='martinikimi7@gmail.com',
            to=[order.user.email],
            reply_to=['martinikimi7@gmail.com']
        )
        
        email.attach_alternative(html_content, "text/html")
        email.send()
        
        print(f"✅ Order status update sent to CUSTOMER: {order.user.email}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send order status update: {e}")
        return False

def send_order_shipped_notification(order):
    """
    Special notification when order is shipped
    """
    try:
        subject = f"🚚 Your Order Has Shipped! - #{order.order_number}"
        
        html_content = render_to_string(
            'emails/order_shipped.html',
            {
                'order': order,
                'order_items': order.items.all(),
                'store_name': 'NexusStore',
                'support_email': 'martinikimi7@gmail.com'
            }
        )
        
        text_content = strip_tags(html_content)
        
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email='martinikimi7@gmail.com',
            to=[order.user.email],
            reply_to=['martinikimi7@gmail.com']
        )
        
        email.attach_alternative(html_content, "text/html")
        email.send()
        
        print(f" Order shipped notification sent to CUSTOMER: {order.user.email}")
        return True
        
    except Exception as e:
        print(f" Failed to send shipped notification: {e}")
        return False