import random
import logging
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)

def generate_otp(length=6):
    """
    Generates a random OTP code of the specified length (default 6 digits).
    """
    digits = "0123456789"
    otp = ''.join(random.choice(digits) for _ in range(length))
    return otp

def send_email(subject, message, recipient_list, html_message=None):
    """
    Helper function to send emails with optional HTML content.
    """
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            recipient_list,
            html_message=html_message
        )
        logger.info(f"Email sent to {recipient_list}")
    except Exception as e:
        logger.error(f"Failed to send email to {recipient_list}: {str(e)}")

def send_otp_email(email, otp_code, subject="Your OTP Code for Email Verification"):
    """
    Sends the provided OTP code to the user's email address with a customizable subject.
    """
    html_message = OTP_EMAIL_TEMPLATE.format(otp_code=otp_code)
    message = strip_tags(html_message)
    send_email(subject, message, [email], html_message=html_message)

def send_registration_email(email):
    """
    Sends a registration email to the provided email address.
    """
    subject = "Welcome to Our Platform!"
    html_message = REGISTRATION_EMAIL_TEMPLATE.format(email=email)
    message = strip_tags(html_message)
    send_email(subject, message, [email], html_message=html_message)

def send_password_reset_email(email, reset_link):
    """
    Sends a password reset email to the provided email address with the reset link.
    """
    subject = "Password Reset Request"
    html_message = PASSWORD_RESET_EMAIL_TEMPLATE.format(reset_link=reset_link)
    message = strip_tags(html_message)
    send_email(subject, message, [email], html_message=html_message)

# Email Templates
OTP_EMAIL_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Your OTP Code</title>
</head>
<body>
    <p>Your OTP code is: {otp_code}</p>
</body>
</html>
"""

REGISTRATION_EMAIL_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Welcome to Our Platform!</title>
</head>
<body>
    <p>Thank you for registering with us, {email}. We're excited to have you on board!</p>
</body>
</html>
"""

PASSWORD_RESET_EMAIL_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Password Reset Request</title>
</head>
<body>
    <p>Please click on the following link to reset your password:</p>
    <a href="{reset_link}">Reset Password</a>
</body>
</html>
"""

