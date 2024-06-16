from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Tag, Article, BlogPost, Image, Video, Document

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class TagSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField(
        max_length=50,
        validators=[
            serializers.UniqueValidator(queryset=Tag.objects.all(), message="Tag with this name already exists.")
        ]
    )

    class Meta:
        model = Tag
        fields = ['url', 'id', 'name']

class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    title = serializers.CharField(max_length=200)
    content = serializers.CharField()
    reading_time = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['url', 'id', 'title', 'content', 'author', 'created_at', 'updated_at', 'tags', 'reading_time']
        read_only_fields = ['created_at', 'updated_at']

    def get_reading_time(self, obj):
        word_count = len(obj.content.split())
        reading_time = word_count // 200  # Assuming an average reading speed of 200 words per minute
        return f"{reading_time} min read"

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long.")
        return value

    def validate(self, data):
        if 'Django' not in data['content']:
            raise serializers.ValidationError("Content must mention 'Django'.")
        return data

class BlogPostSerializer(serializers.HyperlinkedModelSerializer):
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    title = serializers.CharField(max_length=200)
    content = serializers.CharField()
    reading_time = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = ['url', 'id', 'title', 'content', 'author', 'created_at', 'updated_at', 'tags', 'reading_time']
        read_only_fields = ['created_at', 'updated_at']

    def get_reading_time(self, obj):
        word_count = len(obj.content.split())
        reading_time = word_count // 200  # Assuming an average reading speed of 200 words per minute
        return f"{reading_time} min read"

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long.")
        return value

    def validate(self, data):
        if 'Django' not in data['content']:
            raise serializers.ValidationError("Content must mention 'Django'.")
        return data

class ImageSerializer(serializers.HyperlinkedModelSerializer):
    uploaded_by = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    thumbnail = serializers.SerializerMethodField()
    preview = serializers.ImageField(read_only=True)
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(allow_blank=True)

    class Meta:
        model = Image
        fields = ['url', 'id', 'title', 'uploaded_by', 'uploaded_at', 'description', 'tags', 'image', 'thumbnail', 'preview']
        read_only_fields = ['uploaded_at']

    def get_thumbnail(self, obj):
        return obj.thumbnail.url if obj.thumbnail else None

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long.")
        return value

class VideoSerializer(serializers.HyperlinkedModelSerializer):
    uploaded_by = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(allow_blank=True)
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ['url', 'id', 'title', 'uploaded_by', 'uploaded_at', 'description', 'tags', 'video', 'thumbnail']
        read_only_fields = ['uploaded_at']

    def get_thumbnail(self, obj):
        # Implement thumbnail generation logic here
        return None

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long.")
        return value

    def validate_video(self, value):
        if value.size > 2500 * 1024 * 1024:  # 2500 MB limit
            raise serializers.ValidationError("Video file size must be under 2500 MB.")
        return value

class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    uploaded_by = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(allow_blank=True)

    class Meta:
        model = Document
        fields = ['url', 'id', 'title', 'uploaded_by', 'uploaded_at', 'description', 'tags', 'document']
        read_only_fields = ['uploaded_at']

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long.")
        return value

    def validate_document(self, value):
        if value.size > 10 * 1024 * 1024:  # 10 MB limit
            raise serializers.ValidationError("Document file size must be under 10 MB.")
        return value

