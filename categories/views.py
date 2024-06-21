from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Category as CategoryModel
from .serializers import CategorySerializer

# 카테고리 정보 조회 API
class Category(APIView):
    def get(self, request, category_id):
        try:
            # 해당 카테고리 id 가지는 카테고리 데이터 조회
            category = CategoryModel.objects.get(category_id = category_id)
        except:
            # 없으면 오류
            raise NotFound
        
        # json 형식으로 변환 후 응답
        serializer = CategorySerializer(category)
        return Response(serializer.data)

