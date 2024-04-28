from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = (
        'user_email',
        'user_name',
        'user_joined_date',
        'user_cash',
        'is_admin',
    )
    ordering = ('user_email',)

admin.site.register(User, CustomUserAdmin)
