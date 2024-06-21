from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from .models import User

# 관리자 패널 설정
class CustomUserAdmin(UserAdmin):
    # 보여줄 컬럼
    list_display = (
        'user_email',
        'user_name',
        'user_joined_date',
        'user_cash',
        'is_admin',
    )
    # 정렬 기준
    ordering = ('user_email',)

admin.site.register(User, CustomUserAdmin)
