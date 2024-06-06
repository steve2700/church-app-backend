from django.urls import path
from .views import (
    UserRegisterView,
    UserProfileUpdateView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    AccountDeleteView,
    CustomLoginView
)

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user_register'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='user_profile_update'),
    path('password/reset/request/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('account/delete/', AccountDeleteView.as_view(), name='account_delete'),
    path('login/', CustomLoginView.as_view(), name='login'),
]

