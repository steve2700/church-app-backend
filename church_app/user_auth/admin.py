# user_auth/admin.py
from django.contrib import admin
from .models import UserProfile, FacebookSocialAccount, GoogleSocialAccount, ChurchBranch

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'membership_status', 'role', 'church_branch')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('membership_status', 'role', 'church_branch')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'date_of_birth', 'profile_picture', 'address', 'phone_number', 'emergency_contact_name', 'emergency_contact_phone_number')}),
        ('Membership', {'fields': ('membership_start_date', 'membership_status', 'role', 'church_branch', 'tithe_amount')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(FacebookSocialAccount)
admin.site.register(GoogleSocialAccount)
admin.site.register(ChurchBranch)

