# user_auth/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .serializers import UserProfileSerializer, UserProfileCreateSerializer
from .utils import generate_otp, send_otp_email, send_registration_email, send_password_reset_email

User = get_user_model()

class UserRegisterView(generics.CreateAPIView):
    """
    API view to handle user registration.
    """
    queryset = User.objects.all()
    serializer_class = UserProfileCreateSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        """
        Override the default behavior to add custom logic after user creation.
        """
        user = serializer.save()

        # Generate OTP code
        otp_code = generate_otp()

        # Save OTP code and expiry time to user model
        user.otp_code = otp_code
        user.otp_code_expiry = timezone.now() + timezone.timedelta(minutes=15)  # OTP expires in 15 minutes
        user.save()

        # Send OTP code to user via email
        send_otp_email(user.email, otp_code)

        # Send registration email
        send_registration_email(user.email)  # Call the function to send registration email

        return user

class UserProfileUpdateView(generics.UpdateAPIView):
    """
    API view to handle updating user profiles.
    """
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Retrieve and return the authenticated user.
        """
        return self.request.user

class PasswordResetRequestView(APIView):
    """
    API view to handle password reset requests.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # Generate password reset link
        current_site = get_current_site(request)
        reset_url = reverse('password_reset_confirm')
        reset_link = f"http://{current_site.domain}{reset_url}?email={email}"  # Example URL, adjust as needed

        # Send password reset email
        send_password_reset_email(user.email, reset_link)  # Call the function to send password reset email

        return Response({'message': 'Password reset email has been sent'})

class PasswordResetConfirmView(APIView):
    """
    API view to handle password reset confirmation.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        otp_code = request.data.get('otp_code')
        new_password = request.data.get('new_password')

        if not all([email, otp_code, new_password]):
            return Response({'error': 'Email, OTP code, and new password are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if otp_code != user.otp_code:
            return Response({'error': 'Invalid OTP code'}, status=status.HTTP_400_BAD_REQUEST)

        if user.is_otp_expired():
            return Response({'error': 'OTP code has expired'}, status=status.HTTP_400_BAD_REQUEST)

        # Update user password
        user.set_password(new_password)
        user.save()

        return Response({'message': 'Password reset successful'})

class AccountDeleteView(APIView):
    """
    API view to handle account deletion.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return Response({'message': 'Account deleted successfully'})

