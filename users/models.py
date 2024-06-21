from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class UserManager(BaseUserManager):
    def _create_user(self, user_email, user_name, password, **extra_fields):
        if not user_email:
            raise ValueError("이메일을 입력하세요")
        if not user_name:
            raise ValueError("이름을 입력하세요.")
        
        user_email = self.normalize_email(user_email)
        user = self.model(
            user_email=user_email, 
            user_name=user_name, 
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, user_email, user_name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(user_email, user_name, password, **extra_fields)
    
    def create_superuser(self, user_email, user_name, password, **extra_fields):
        user = self.create_user(user_email=user_email, password=password, user_name=user_name)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# 유저 모델
class User(AbstractBaseUser, PermissionsMixin):
    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("female", "Female") 

    # 컬럼들
    user_email = models.EmailField(primary_key=True, blank=False)
    user_name = models.CharField(max_length=30, null=False, blank=False)
    user_gender = models.CharField(max_length=10, choices=GenderChoices.choices, null=True, blank=True)
    user_cash = models.IntegerField(default=50000, null=False, blank=True)
    user_birth = models.DateField(null=True, blank=True)
    user_joined_date = models.DateTimeField(default=timezone.now)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # 관리자 로그인 시 형식 지정
    USERNAME_FIELD = "user_email"
    REQUIRED_FIELDS = ['user_name', 'password']

    objects = UserManager()

    def __str__(self):
        return self.user_name
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_lable):
        return True

