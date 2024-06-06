from django.apps import AppConfig
from django.db.models.signals import post_save

class UserAuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "user_auth"

    def ready(self):
        from .models import UserProfile
        from .signals import user_profile_post_save_handler

        # Register post-save signals
        post_save.connect(user_profile_post_save_handler, sender=UserProfile)

