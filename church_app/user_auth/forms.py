from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import UserProfile

class BaseUserProfileForm(forms.ModelForm):
    """
    Base form for UserProfile to be used for common configurations.
    """
    class Meta:
        model = UserProfile
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'membership_start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '+999999999', 'class': 'form-control'}),
            'emergency_contact_phone_number': forms.TextInput(attrs={'placeholder': '+999999999', 'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'username': 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
            'phone_number': 'Phone number must be entered in the format: "+999999999". Up to 15 digits allowed.',
            'emergency_contact_phone_number': 'Phone number must be entered in the format: "+999999999". Up to 15 digits allowed.',
        }

class UserProfileCreationForm(BaseUserProfileForm, UserCreationForm):
    """
    Form for creating a new user profile.
    """
    class Meta(BaseUserProfileForm.Meta, UserCreationForm.Meta):
        fields = ('username', 'email', 'date_of_birth', 'profile_picture', 'address', 'phone_number', 'membership_start_date', 'membership_status', 'role', 'church_branch', 'emergency_contact_name', 'emergency_contact_phone_number', 'tithe_amount')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserProfile.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

class UserProfileChangeForm(BaseUserProfileForm, UserChangeForm):
    """
    Form for updating an existing user profile.
    """
    class Meta(BaseUserProfileForm.Meta, UserChangeForm.Meta):
        fields = ('username', 'email', 'date_of_birth', 'profile_picture', 'address', 'phone_number', 'membership_start_date', 'membership_status', 'role', 'church_branch', 'emergency_contact_name', 'emergency_contact_phone_number', 'tithe_amount')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.instance and self.instance.email != email and UserProfile.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

class CustomAuthenticationForm(AuthenticationForm):
    """
    Custom authentication form for login.
    """
    username = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': 'Email', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Email'

class UserProfileUpdateForm(BaseUserProfileForm):
    """
    Form for updating user profile details.
    """
    class Meta(BaseUserProfileForm.Meta):
        fields = ('first_name', 'last_name', 'email', 'date_of_birth', 'profile_picture', 'address', 'phone_number', 'emergency_contact_name', 'emergency_contact_phone_number')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.instance and self.instance.email != email and UserProfile.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

