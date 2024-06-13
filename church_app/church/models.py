from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from ckeditor.fields import RichTextField  # For rich text descriptions

User = get_user_model()

# Choices for event status
EVENT_STATUS_CHOICES = [
    ('UPCOMING', 'Upcoming'),
    ('ONGOING', 'Ongoing'),
    ('COMPLETED', 'Completed'),
]

class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name="Event Title")
    description = RichTextField()  # Using RichTextField for rich text descriptions
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    attendees = models.ManyToManyField(User, related_name='attended_events', blank=True)
    status = models.CharField(max_length=10, choices=EVENT_STATUS_CHOICES, default='UPCOMING')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['date']  # Order events by date

class Series(models.Model):
    title = models.CharField(max_length=200, verbose_name="Series Title")
    description = RichTextField(blank=True, null=True)  # Using RichTextField for rich text descriptions
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title

class Scripture(models.Model):
    book = models.CharField(max_length=50)
    chapter = models.IntegerField()
    verse = models.IntegerField()

    def __str__(self):
        return f"{self.book} {self.chapter}:{self.verse}"

class Sermon(models.Model):
    title = models.CharField(max_length=200, verbose_name="Sermon Title")
    description = RichTextField()  # Using RichTextField for rich text descriptions
    date = models.DateTimeField()
    speaker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sermons')
    series = models.ForeignKey(Series, on_delete=models.SET_NULL, null=True, blank=True, related_name='sermons')
    scriptures = models.ManyToManyField(Scripture, blank=True, related_name='sermons')
    audio_file = models.FileField(upload_to='sermons/audio/', validators=[FileExtensionValidator(['mp3', 'wav'])], verbose_name="Audio Sermon", blank=True, null=True)
    video_file = models.FileField(upload_to='sermons/video/', validators=[FileExtensionValidator(['mp4', 'mkv'])], verbose_name="Video Sermon", blank=True, null=True)
    transcript = models.TextField(blank=True, null=True)  # Store automated transcripts here
    slides = models.FileField(upload_to='sermons/slides/', validators=[FileExtensionValidator(['pdf', 'ppt', 'pptx'])], verbose_name="Slides", blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['date']  # Order sermons by date

class RatingReview(models.Model):
    sermon = models.ForeignKey(Sermon, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sermon.title} - {self.user.username}"

class Note(models.Model):
    sermon = models.ForeignKey(Sermon, on_delete=models.CASCADE, related_name='notes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    timestamp = models.DateTimeField(auto_now_add=True)
    note = models.TextField()

    def __str__(self):
        return f"Note by {self.user.username} on {self.sermon.title} at {self.timestamp}"

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True, validators=[MinLengthValidator(10)])
    address = models.CharField(max_length=300, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

