from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import UserProfile

@receiver(post_save, sender=UserProfile)
def user_profile_post_save_handler(sender, instance, created, **kwargs):
    if created:
        # Send a welcome email upon user creation
        subject = 'Welcome to Our Church!'
        message = f'Hi {instance.first_name},\n\nWelcome to our church community! We are glad to have you with us.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.email]
        send_mail(subject, message, from_email, recipient_list)

