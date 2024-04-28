from rest_framework.serializers import ModelSerializer
from .models import User

class SignUpSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "user_email",
            "password",
            "user_name",
            "user_gender",
            "user_birth",
        )

class LogInSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "user_email",
            "password"
        )

class UserInfoSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "user_name",
            "user_cash",
        )