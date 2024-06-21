from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Author

# 작가 데이터 json 형식 지정
class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        # 모든 컬럼 다 나오게
        fields = "__all__"