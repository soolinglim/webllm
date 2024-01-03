from django.contrib import admin
from .models import *

# Register your models here.
class UserInputAdmin(admin.ModelAdmin):
    # fields = ('access_key', 'name')
    list_display = ('pk', 'user_input', 'hide',)
    ordering = ('-timestamp',)

admin.site.register(UserInput, UserInputAdmin)
