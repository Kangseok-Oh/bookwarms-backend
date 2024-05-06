from rest_framework.serializers import ModelSerializer
from .models import User

class UserInfoSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "user_name",
            "user_cash",
        )