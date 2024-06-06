from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models
from django.core.validators import RegexValidator, EmailValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from allauth.socialaccount.models import SocialAccount
from dirtyfields import DirtyFieldsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import phonenumbers
import logging

logger = logging.getLogger(__name__)

class UserProfileManager(BaseUserManager):
    """
    Custom user manager for UserProfile model.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

class UserProfile(AbstractUser, DirtyFieldsMixin):
    """
    Extended user model with additional fields for church application.
    """
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message=_("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))]
    )
    membership_start_date = models.DateField(blank=True, null=True)
    membership_status = models.CharField(
        max_length=20,
        choices=[
            ('active', _('Active')),
            ('inactive', _('Inactive')),
            ('pending', _('Pending')),
            ('suspended', _('Suspended'))
        ],
        default='pending'
    )
    role = models.CharField(
        max_length=50,
        choices=[
            ('member', _('Member')),
            ('staff', _('Staff')),
            ('pastor', _('Pastor')),
            ('admin', _('Admin'))
        ],
        default='member'
    )
    church_branch = models.ForeignKey('ChurchBranch', on_delete=models.SET_NULL, null=True, blank=True)
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    otp_code_expiry = models.DateTimeField(blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=255, blank=True, null=True)
    emergency_contact_phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message=_("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))]
    )
    tithe_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    objects = UserProfileManager()

    # Add custom related names to avoid clashes
    @property
    def custom_user_groups(self):
        return self.groups

    @property
    def custom_user_permissions(self):
        return self.user_permissions

    def __str__(self):
        return self.username

    def is_otp_valid(self):
        """
        Check if the OTP code is still valid.
        """
        return self.otp_code_expiry and self.otp_code_expiry > timezone.now()

    def get_full_address(self):
        """
        Return the user's full address.
        """
        return f'{self.address}'

    def is_member_active(self):
        """
        Check if the user is an active member.
        """
        return self.membership_status == 'active'

class FacebookSocialAccount(models.Model):
    """
    Model to store Facebook social account information.
    """
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='facebook_social_accounts')
    social_account = models.ForeignKey(SocialAccount, on_delete=models.CASCADE)
    social_account_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - Facebook'

class GoogleSocialAccount(models.Model):
    """
    Model to store Google social account information.
    """
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='google_social_accounts')
    social_account = models.ForeignKey(SocialAccount, on_delete=models.CASCADE)
    social_account_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - Google'

class ChurchBranch(models.Model):
    """
    Model to store information about church branches.
    """
    name = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.name

@receiver(post_save, sender=UserProfile)
def post_save_user_profile(sender, instance, created, **kwargs):
    """
    Signal to perform actions after a user profile is saved.
    """
    if created:
        try:
            subject = _('Welcome to Our Church!')
            message = _(f'Hi {instance.first_name},\n\nWelcome to our church community! We are glad to have you with us.')
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [instance.email]
            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            logger.error(f'Error sending welcome email to {instance.email}: {e}')

@receiver(post_save, sender=UserProfile)
def post_save_membership_status(sender, instance, **kwargs):
    """
    Signal to perform actions when membership status changes.
    """
    if 'membership_status' in instance.get_dirty_fields():
        try:
            logger.info(f"User {instance.username}'s membership status changed to {instance.membership_status}.")
            # Add additional logic here, e.g., notifying staff
        except Exception as e:
            logger.error(f'Error handling membership status change for {instance.username}: {e}')

