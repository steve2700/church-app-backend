from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField

User = get_user_model()

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_("Name"))

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        ordering = ['name']

    def __str__(self):
        return self.name

class Content(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("Title"))
    content = RichTextField(verbose_name=_("Content"))
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Author"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    tags = models.ManyToManyField(Tag, blank=True, verbose_name=_("Tags"))

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['title'], name='content_title_idx'),
        ]

    def __str__(self):
        return self.title

class Article(Content):
    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")
        ordering = ['-created_at']

class BlogPost(Content):
    class Meta:
        verbose_name = _("Blog Post")
        verbose_name_plural = _("Blog Posts")
        ordering = ['-created_at']

class Image(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("Title"))
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Uploaded By"))
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Uploaded At"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    tags = models.ManyToManyField(Tag, blank=True, verbose_name=_("Tags"))
    image = models.ImageField(upload_to='images/', verbose_name=_("Image"))

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")
        ordering = ['-uploaded_at']
        unique_together = ('title', 'uploaded_by')

    def __str__(self):
        return self.title

    @property
    def thumbnail(self):
        from PIL import Image as PILImage
        from io import BytesIO
        from django.core.files.uploadedfile import InMemoryUploadedFile

        if self.image:
            img = PILImage.open(self.image)
            img.thumbnail((100, 100), PILImage.ANTIALIAS)
            thumb_io = BytesIO()
            img.save(thumb_io, format='JPEG')
            thumbnail = InMemoryUploadedFile(thumb_io, None, 'thumbnail.jpg', 'image/jpeg', thumb_io.getbuffer().nbytes, None)
            return thumbnail
        return None

class Video(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("Title"))
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Uploaded By"))
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Uploaded At"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    tags = models.ManyToManyField(Tag, blank=True, verbose_name=_("Tags"))
    video = models.FileField(upload_to='videos/', verbose_name=_("Video"))

    class Meta:
        verbose_name = _("Video")
        verbose_name_plural = _("Videos")
        ordering = ['-uploaded_at']
        unique_together = ('title', 'uploaded_by')

    def __str__(self):
        return self.title

class Document(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("Title"))
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Uploaded By"))
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Uploaded At"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    tags = models.ManyToManyField(Tag, blank=True, verbose_name=_("Tags"))
    document = models.FileField(upload_to='documents/', verbose_name=_("Document"))

    class Meta:
        verbose_name = _("Document")
        verbose_name_plural = _("Documents")
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title

