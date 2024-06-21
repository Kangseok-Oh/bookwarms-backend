from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Category

# 카테고리 json 형식 지정
class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        # 모든 컬럼 다 호출
        fields = "__all__"