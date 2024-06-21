from rest_framework.serializers import ModelSerializer
from .models import User

# 헤더에서 보여줄 유저 데이터 형식 지정
class UserInfoSerializer(ModelSerializer):
    class Meta:
        model = User
        # 보낼 컬럼들
        fields = (
            "user_name",
            "user_cash",
        )