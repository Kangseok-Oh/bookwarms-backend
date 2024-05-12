from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Category as CategoryModel
from .serializers import CategorySerializer

class Category(APIView):
    def get(self, request, category_id):
        try:
            category = CategoryModel.objects.get(category_id = category_id)
        except:
            raise NotFound
        serializer = CategorySerializer(category)
        return Response(serializer.data)

