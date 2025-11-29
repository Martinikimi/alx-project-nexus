import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_email_system():
    print("Testing email configuration...")
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print(f"ADMIN_EMAIL: {settings.ADMIN_EMAIL}")
    
    try:
        # Test sending email
        send_mail(
            'Test Email from E-commerce',
            'This is a test email to verify your email configuration is working!',
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=False,
        )
        print("✅ Test email sent successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to send test email: {e}")
        return False

if __name__ == "__main__":
    test_email_system()