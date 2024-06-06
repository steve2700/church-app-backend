import logging
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .serializers import UserProfileSerializer, UserProfileCreateSerializer, CustomAuthTokenSerializer, PasswordResetRequestSerializer,  PasswordResetConfirmSerializer, FacebookSocialAccountSerializer, GoogleSocialAccountSerializer , ChurchBranchSerializer, UserTokenSerializer
from .utils import generate_otp, send_otp_email, send_registration_email, send_password_reset_email
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
User = get_user_model()

logger = logging.getLogger(__name__)

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
        send_registration_email(user.email)

        logger.info(f"User registered with email: {user.email}")

        return user
class CustomLoginView(ObtainAuthToken):
    """
    API view to handle user login and return the authentication token.
    """
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        }, status=status.HTTP_200_OK)

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

    def perform_update(self, serializer):
        """
        Override the default behavior to add custom logic after user update.
        """
        user = serializer.save()
        logger.info(f"User profile updated: {user.email}")
        return user

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
        reset_link = f"http://{current_site.domain}{reset_url}?email={email}"

        # Send password reset email
        send_password_reset_email(user.email, reset_link)

        logger.info(f"Password reset requested for email: {user.email}")

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

        # Add password complexity check
        if len(new_password) < 8:
            return Response({'error': 'Password must be at least 8 characters long'}, status=status.HTTP_400_BAD_REQUEST)

        # Update user password
        user.set_password(new_password)
        user.save()

        logger.info(f"Password reset successful for email: {user.email}")

        return Response({'message': 'Password reset successful'})

class AccountDeleteView(APIView):
    """
    API view to handle account deletion.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        Token.objects.filter(user=user).delete()
        user.delete()
        logger.info(f"Account deleted for user: {user.email}")
        return Response({'message': 'Account deleted successfully'})

class UserProfileRetrieveView(generics.RetrieveAPIView):
    """
    API view to retrieve user profile.
    """
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Retrieve and return the authenticated user.
        """
        return self.request.user

