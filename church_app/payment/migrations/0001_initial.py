# Generated by Django 5.0.2 on 2024-06-18 14:10

import django.core.validators
import django.db.models.deletion
import encrypted_model_fields.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="PaymentMethod",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "method_name",
                    models.CharField(max_length=50, verbose_name="Payment Method Name"),
                ),
                (
                    "card_number",
                    encrypted_model_fields.fields.EncryptedCharField(
                        verbose_name="Card Number"
                    ),
                ),
                ("expiration_date", models.DateField(verbose_name="Expiration Date")),
                (
                    "cardholder_name",
                    models.CharField(max_length=100, verbose_name="Cardholder Name"),
                ),
                (
                    "cvv",
                    encrypted_model_fields.fields.EncryptedCharField(
                        verbose_name="CVV"
                    ),
                ),
                ("billing_address", models.TextField(verbose_name="Billing Address")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated At"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payment_methods",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "transaction_type",
                    models.CharField(
                        choices=[("donation", "Donation")],
                        default="donation",
                        max_length=20,
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10,
                        validators=[django.core.validators.MinValueValidator(0.01)],
                        verbose_name="Amount",
                    ),
                ),
                (
                    "currency",
                    models.CharField(
                        default="USD", max_length=3, verbose_name="Currency"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("completed", "Completed"),
                            ("failed", "Failed"),
                            ("refunded", "Refunded"),
                        ],
                        default="pending",
                        max_length=20,
                        verbose_name="Status",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated At"),
                ),
                (
                    "payment_gateway",
                    models.CharField(max_length=50, verbose_name="Payment Gateway"),
                ),
                (
                    "transaction_id",
                    models.CharField(max_length=100, verbose_name="Transaction ID"),
                ),
                (
                    "gateway_response_code",
                    models.CharField(
                        max_length=50, verbose_name="Gateway Response Code"
                    ),
                ),
                (
                    "gateway_response_message",
                    models.TextField(
                        blank=True, null=True, verbose_name="Gateway Response Message"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="transactions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Refund",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10,
                        validators=[django.core.validators.MinValueValidator(0.01)],
                        verbose_name="Amount",
                    ),
                ),
                (
                    "reason",
                    models.TextField(blank=True, null=True, verbose_name="Reason"),
                ),
                (
                    "processed_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Processed At"
                    ),
                ),
                (
                    "transaction",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="refund",
                        to="payment.transaction",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Donation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "recurring",
                    models.BooleanField(default=False, verbose_name="Recurring"),
                ),
                (
                    "frequency",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("monthly", "Monthly"),
                            ("weekly", "Weekly"),
                            ("yearly", "Yearly"),
                        ],
                        max_length=20,
                        null=True,
                        verbose_name="Frequency",
                    ),
                ),
                (
                    "start_date",
                    models.DateField(blank=True, null=True, verbose_name="Start Date"),
                ),
                (
                    "end_date",
                    models.DateField(blank=True, null=True, verbose_name="End Date"),
                ),
                (
                    "transaction",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="donation",
                        to="payment.transaction",
                    ),
                ),
            ],
        ),
    ]