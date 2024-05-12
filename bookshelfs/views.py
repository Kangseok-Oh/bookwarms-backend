from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from .models import BookshelfItem
from .serializers import BookshelfListSerializer

class BookshelfList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user_email = request.user.user_email
        try:
            bookshelf_list = BookshelfItem.objects.filter(bookshelf_user_email = user_email)
        except:
            raise NotFound
        serializer = BookshelfListSerializer(bookshelf_list, many = True)
        return Response(serializer.data)