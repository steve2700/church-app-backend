from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from encrypted_model_fields.fields import EncryptedCharField

User = get_user_model()

class PaymentMethod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_methods')
    method_name = models.CharField(max_length=50, verbose_name=_("Payment Method Name"))  # e.g., Credit Card, PayPal
    card_number = EncryptedCharField(max_length=16, verbose_name=_("Card Number"))
    expiration_date = models.DateField(verbose_name=_("Expiration Date"))
    cardholder_name = models.CharField(max_length=100, verbose_name=_("Cardholder Name"))
    cvv = EncryptedCharField(max_length=4, verbose_name=_("CVV"))
    billing_address = models.TextField(verbose_name=_("Billing Address"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    def __str__(self):
        return f"{self.method_name} ending in {self.card_number[-4:]} for {self.user.username}"

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('donation', _('Donation')),
    ]

    TRANSACTION_STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('completed', _('Completed')),
        ('failed', _('Failed')),
        ('refunded', _('Refunded')),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES, default='donation')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)], verbose_name=_("Amount"))
    currency = models.CharField(max_length=3, default='USD', verbose_name=_("Currency"))
    status = models.CharField(max_length=20, choices=TRANSACTION_STATUS_CHOICES, default='pending', verbose_name=_("Status"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    payment_gateway = models.CharField(max_length=50, verbose_name=_("Payment Gateway"))  # e.g., Stripe, PayPal
    transaction_id = models.CharField(max_length=100, verbose_name=_("Transaction ID"))
    gateway_response_code = models.CharField(max_length=50, verbose_name=_("Gateway Response Code"))
    gateway_response_message = models.TextField(blank=True, null=True, verbose_name=_("Gateway Response Message"))

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} {self.currency} by {self.user.username}"

class Donation(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='donation')
    recurring = models.BooleanField(default=False, verbose_name=_("Recurring"))
    frequency = models.CharField(max_length=20, choices=[('monthly', 'Monthly'), ('weekly', 'Weekly'), ('yearly', 'Yearly')], blank=True, null=True, verbose_name=_("Frequency"))
    start_date = models.DateField(blank=True, null=True, verbose_name=_("Start Date"))
    end_date = models.DateField(blank=True, null=True, verbose_name=_("End Date"))

    def __str__(self):
        return f"Donation of {self.transaction.amount} {self.transaction.currency} by {self.transaction.user.username}"

class Refund(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='refund')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)], verbose_name=_("Amount"))
    reason = models.TextField(blank=True, null=True, verbose_name=_("Reason"))
    processed_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Processed At"))

    def __str__(self):
        return f"Refund of {self.amount} {self.transaction.currency} for transaction {self.transaction.transaction_id}"

