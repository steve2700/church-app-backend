from rest_framework import serializers
from .models import Event, Series, Scripture, Sermon, RatingReview, Note, Member
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models import Q

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ScriptureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scripture
        fields = ['id', 'book', 'chapter', 'verse']

class SeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = ['id', 'title', 'description', 'start_date', 'end_date']

class EventSerializer(serializers.ModelSerializer):
    organizer = UserSerializer(read_only=True)
    attendees = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'location', 'organizer', 'attendees', 'status']
        read_only_fields = ('id', 'organizer', 'attendees')

    def create(self, validated_data):
        request = self.context.get('request')
        organizer = request.user if request else None
        event = Event.objects.create(organizer=organizer, **validated_data)
        return event

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.date = validated_data.get('date', instance.date)
        instance.location = validated_data.get('location', instance.location)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

    def validate(self, attrs):
        if attrs.get('status') == 'COMPLETED' and attrs.get('date') > timezone.now():
            raise serializers.ValidationError("Completed events cannot have a future date")
        if attrs.get('date') and attrs.get('end_date') and attrs.get('date') > attrs.get('end_date'):
            raise serializers.ValidationError("Event start date must be before end date")
        return attrs

class SermonSerializer(serializers.ModelSerializer):
    speaker = UserSerializer(read_only=True)
    series = SeriesSerializer(read_only=True)
    scriptures = ScriptureSerializer(many=True, read_only=True)

    class Meta:
        model = Sermon
        fields = ['id', 'title', 'description', 'date', 'speaker', 'series', 'scriptures', 'audio_file', 'video_file', 'transcript', 'slides']
        read_only_fields = ('id', 'speaker', 'series', 'scriptures')

    def create(self, validated_data):
        request = self.context.get('request')
        speaker = request.user if request else None
        sermon = Sermon.objects.create(speaker=speaker, **validated_data)
        return sermon

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.date = validated_data.get('date', instance.date)
        instance.audio_file = validated_data.get('audio_file', instance.audio_file)
        instance.video_file = validated_data.get('video_file', instance.video_file)
        instance.transcript = validated_data.get('transcript', instance.transcript)
        instance.slides = validated_data.get('slides', instance.slides)
        instance.save()
        return instance

    def validate(self, attrs):
        if attrs.get('audio_file') and attrs.get('video_file'):
            raise serializers.ValidationError("Please upload either an audio file or a video file, not both")
        return attrs

class RatingReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingReview
        fields = ['id', 'sermon', 'user', 'rating', 'comment', 'date_created']
        read_only_fields = ('id', 'user', 'date_created')

    def validate(self, attrs):
        # Custom validation logic
        if attrs.get('rating') < 1 or attrs.get('rating') > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return attrs

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'sermon', 'user', 'timestamp', 'note']
        read_only_fields = ('id', 'user', 'timestamp')

    def validate(self, attrs):
        # Custom validation logic
        if attrs.get('note') == "":
            raise serializers.ValidationError("Note cannot be empty")
        return attrs

class MemberSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Member
        fields = ['id', 'user', 'phone_number', 'address', 'date_joined']
        read_only_fields = ('id', 'date_joined')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        member = Member.objects.create(user=user, **validated_data)
        return member

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user
        user.username = user_data.get('username', user.username)
        user.email = user_data.get('email', user.email)
        user.save()

        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.address = validated_data.get('address', instance.address)
        instance.save()

        return instance

    def validate(self, attrs):
        # Custom validation logic
        phone_number = attrs.get('phone_number')
        if phone_number and len(phone_number) < 10:
            raise serializers.ValidationError("Phone number must be at least 10 characters")
        return attrs

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data
        return representation

