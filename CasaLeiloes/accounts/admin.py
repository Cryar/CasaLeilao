from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'is_admin']
    # Add other fields to list_display as needed

admin.site.register(CustomUser, CustomUserAdmin)