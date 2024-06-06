# utils.py
import random
from django.core.mail import send_mail
from django.conf import settings

def generate_otp(length=6):
    """
    Generates a random OTP code of the specified length (default 6 digits).
    """
    digits = "0123456789"
    otp = ''.join(random.choice(digits) for _ in range(length))
    return otp

def send_otp_email(email, otp_code, subject="Your OTP Code for Email Verification"):
    """
    Sends the provided OTP code to the user's email address with a customizable subject.
    """
    message = f"Your OTP code is: {otp_code}"
    sender_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, sender_email, recipient_list)

def send_registration_email(email):
    """
    Sends a registration email to the provided email address.
    """
    subject = "Welcome to Our Platform!"
    message = "Thank you for registering with us. We're excited to have you on board!"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

def send_password_reset_email(email, reset_link):
    """
    Sends a password reset email to the provided email address with the reset link.
    """
    subject = "Password Reset Request"
    message = f"Please click on the following link to reset your password: {reset_link}"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

