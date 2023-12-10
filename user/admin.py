from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# from django.contrib.auth import get_user_model
# User = get_user_model()

from .forms import UserChangeForm, UserCreationForm
from .models import *

class UserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        # (('Personal info'), {'fields': ('first_name', 'last_name', )}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
            'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
        )
    add_fieldsets = (
        (None, {
        'classes': ('wide',),
        'fields': ('email', 'password1', 'password2'),
        }),
        )
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'is_staff', 'is_active',)
    search_fields = ('email',)
    ordering = ('email',)

# Register the new UserAdmin
admin.site.register(User, UserAdmin)

