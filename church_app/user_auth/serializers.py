from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from .models import UserProfile, FacebookSocialAccount, GoogleSocialAccount, ChurchBranch
from django.contrib.auth import authenticate
User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving and updating user profiles.
    """
    class Meta:
        model = UserProfile
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'date_of_birth', 'profile_picture', 'address', 'phone_number',
            'membership_start_date', 'membership_status', 'role',
            'church_branch', 'emergency_contact_name', 'emergency_contact_phone_number',
            'tithe_amount'
        )

class UserProfileCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new user profile.
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UserProfile
        fields = (
            'username', 'email', 'first_name', 'last_name', 'date_of_birth',
            'profile_picture', 'address', 'phone_number', 'password', 'password2',
            'membership_start_date', 'membership_status', 'role', 'church_branch',
            'emergency_contact_name', 'emergency_contact_phone_number', 'tithe_amount'
        )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = UserProfile.objects.create_user(**validated_data)
        return user

class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset.
    """
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for confirming a password reset.
    """
    email = serializers.EmailField()
    otp_code = serializers.CharField()
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    new_password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs

class FacebookSocialAccountSerializer(serializers.ModelSerializer):
    """
    Serializer for Facebook social account information.
    """
    class Meta:
        model = FacebookSocialAccount
        fields = ('user', 'social_account', 'social_account_id')

class GoogleSocialAccountSerializer(serializers.ModelSerializer):
    """
    Serializer for Google social account information.
    """
    class Meta:
        model = GoogleSocialAccount
        fields = ('user', 'social_account', 'social_account_id')

class ChurchBranchSerializer(serializers.ModelSerializer):
    """
    Serializer for church branch information.
    """
    class Meta:
        model = ChurchBranch
        fields = ('id', 'name', 'address')

class UserTokenSerializer(serializers.Serializer):
    """
    Serializer for user authentication tokens.
    """
    token = serializers.CharField()
    user = UserProfileSerializer()

class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(label="Email")
    password = serializers.CharField(label="Password", style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)

            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

