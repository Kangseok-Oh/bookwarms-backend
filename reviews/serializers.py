from rest_framework.serializers import ModelSerializer
from .models import Review

class reviewItemSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = (
            "review_user_email",
            "review_rating",
            "review_content",
        )