import resend
from django.conf import settings
from django.template.loader import render_to_string

# Configure Resend
resend.api_key = settings.RESEND_API_KEY

def send_order_confirmation(order):
    """
    Send order confirmation email to customer using Resend
    """
    try:
        if not order.user.email:
            print(" No email address for user")
            return False
            
        print(f" Sending order confirmation to: {order.user.email}")
        
        context = {
            'order': order,
            'items': order.items.all(),
            'customer_name': order.user.username,
            'settings': {
                'DEFAULT_FROM_EMAIL': 'martinikimi7@gmail.com'
            }
        }
        
        html_content = render_to_string('emails/order_confirmation.html', context)
        subject = f" Order Confirmed! - #{order.order_number}"
        
        r = resend.Emails.send({
            "from": "ALX Project Nexus <onboarding@resend.dev>",
            "to": [order.user.email],
            "subject": subject,
            "html": html_content,
        })
        
        print(f" Order confirmation email sent successfully! ID: {r['id']}")
        return True
        
    except Exception as e:
        print(f" Failed to send order confirmation: {e}")
        return False

def send_new_order_notification(order):
    """
    Send new order notification to admin using Resend
    """
    try:
        admin_email = "martinikimi7@gmail.com"
        
        print(f" Sending admin notification to: {admin_email}")
        
        context = {
            'order': order,
            'items': order.items.all(),
            'customer_name': order.user.username,
        }
        
        html_content = render_to_string('emails/new_order_notification.html', context)
        subject = f" New Order Received - #{order.order_number}"
        
        r = resend.Emails.send({
            "from": "ALX Project Nexus <onboarding@resend.dev>",
            "to": [admin_email],
            "subject": subject,
            "html": html_content,
        })
        
        print(f" Admin notification sent successfully! ID: {r['id']}")
        return True
        
    except Exception as e:
        print(f" Failed to send admin notification: {e}")
        return False

def send_order_status_update(order):
    """
    Send email to customer when order status changes using Resend
    """
    try:
        if not order.user.email:
            print(" No email address for user")
            return False
            
        print(f" Sending status update to: {order.user.email}")
        
        context = {
            'order': order,
            'items': order.items.all(),
            'customer_name': order.user.username,
            'settings': {
                'DEFAULT_FROM_EMAIL': 'martinikimi7@gmail.com'
            }
        }
        
        html_content = render_to_string('emails/order_status_update.html', context)
        subject = f" Order Update - #{order.order_number}"
        
        r = resend.Emails.send({
            "from": "ALX Project Nexus <onboarding@resend.dev>",
            "to": [order.user.email],
            "subject": subject,
            "html": html_content,
        })
        
        print(f" Order status update sent successfully! ID: {r['id']}")
        return True
        
    except Exception as e:
        print(f" Failed to send order status update: {e}")
        return False

def send_order_shipped_notification(order):
    """
    Special notification when order is shipped using Resend
    """
    try:
        if not order.user.email:
            print("❌ No email address for user")
            return False
            
        print(f" Sending shipped notification to: {order.user.email}")
        
        context = {
            'order': order,
            'items': order.items.all(),
            'customer_name': order.user.username,
            'settings': {
                'DEFAULT_FROM_EMAIL': 'martinikimi7@gmail.com'
            }
        }
        
        html_content = render_to_string('emails/order_shipped.html', context)
        subject = f" Your Order Has Shipped! - #{order.order_number}"
        
        r = resend.Emails.send({
            "from": "ALX Project Nexus <onboarding@resend.dev>",
            "to": [order.user.email],
            "subject": subject,
            "html": html_content,
        })
        
        print(f" Order shipped notification sent successfully! ID: {r['id']}")
        return True
        
    except Exception as e:
        print(f" Failed to send shipped notification: {e}")
        return False

def send_test_email():
    """
    Send a test email to verify Resend is working
    """
    try:
        r = resend.Emails.send({
            "from": "ALX Project Nexus <onboarding@resend.dev>",
            "to": ["martinikimi7@gmail.com"],
            "subject": "Test Email from ALX Project Nexus",
            "html": "<strong>Congratulations! Your email system is working perfectly! 🎉</strong>",
        })
        
        print(f" Test email sent successfully! ID: {r['id']}")
        return True
        
    except Exception as e:
        print(f" Failed to send test email: {e}")
        return False