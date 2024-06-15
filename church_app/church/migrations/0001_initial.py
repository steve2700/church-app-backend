# Generated by Django 5.0.2 on 2024-06-15 14:41

import ckeditor_uploader.fields
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Scripture",
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
                ("book", models.CharField(max_length=50)),
                ("chapter", models.IntegerField()),
                ("verse", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Series",
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
                    "title",
                    models.CharField(max_length=200, verbose_name="Series Title"),
                ),
                (
                    "description",
                    ckeditor_uploader.fields.RichTextUploadingField(
                        blank=True, null=True
                    ),
                ),
                ("start_date", models.DateField(blank=True, null=True)),
                ("end_date", models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Event",
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
                ("title", models.CharField(max_length=200, verbose_name="Event Title")),
                ("description", ckeditor_uploader.fields.RichTextUploadingField()),
                ("date", models.DateTimeField()),
                ("location", models.CharField(max_length=200)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("UPCOMING", "Upcoming"),
                            ("ONGOING", "Ongoing"),
                            ("COMPLETED", "Completed"),
                        ],
                        default="UPCOMING",
                        max_length=10,
                    ),
                ),
                (
                    "attendees",
                    models.ManyToManyField(
                        blank=True,
                        related_name="attended_events",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "organizer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="organized_events",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["date"],
            },
        ),
        migrations.CreateModel(
            name="Member",
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
                    "phone_number",
                    models.CharField(
                        blank=True,
                        max_length=15,
                        null=True,
                        validators=[django.core.validators.MinLengthValidator(10)],
                    ),
                ),
                ("address", models.CharField(blank=True, max_length=300, null=True)),
                ("date_joined", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Sermon",
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
                    "title",
                    models.CharField(max_length=200, verbose_name="Sermon Title"),
                ),
                ("description", ckeditor_uploader.fields.RichTextUploadingField()),
                ("date", models.DateTimeField()),
                (
                    "audio_file",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="sermons/audio/",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                ["mp3", "wav"]
                            )
                        ],
                        verbose_name="Audio Sermon",
                    ),
                ),
                (
                    "video_file",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="sermons/video/",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                ["mp4", "mkv"]
                            )
                        ],
                        verbose_name="Video Sermon",
                    ),
                ),
                ("transcript", models.TextField(blank=True, null=True)),
                (
                    "slides",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="sermons/slides/",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                ["pdf", "ppt", "pptx"]
                            )
                        ],
                        verbose_name="Slides",
                    ),
                ),
                (
                    "scriptures",
                    models.ManyToManyField(
                        blank=True, related_name="sermons", to="church.scripture"
                    ),
                ),
                (
                    "series",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="sermons",
                        to="church.series",
                    ),
                ),
                (
                    "speaker",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sermons",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["date"],
            },
        ),
        migrations.CreateModel(
            name="RatingReview",
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
                ("rating", models.PositiveSmallIntegerField()),
                ("comment", models.TextField(blank=True, null=True)),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reviews",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "sermon",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reviews",
                        to="church.sermon",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Note",
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
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                ("note", models.TextField()),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notes",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "sermon",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notes",
                        to="church.sermon",
                    ),
                ),
            ],
        ),
    ]
