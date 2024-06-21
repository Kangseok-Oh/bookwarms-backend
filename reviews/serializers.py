from rest_framework.serializers import ModelSerializer
from .models import Review

# 리뷰 리스트 출력용 리뷰 데이터 json 형식 지정
class reviewItemSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = (
            "review_user_email",
            "review_rating",
            "review_content",
        )