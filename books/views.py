from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Book
from .serializers import BookDetailSerializer, CategoryBookListSerializer

class CategoryBookList(APIView):
    def get(self, request, category_id):
        try:
            books = Book.objects.filter(book_category_id = category_id)
        except:
            raise NotFound
        serializer = CategoryBookListSerializer(books, many=True)
        return Response(serializer.data)
    
class BookDetail(APIView):
    def get(self, request, book_isbn):
        try:
            book = Book.objects.get(book_isbn = book_isbn)
        except:
            raise NotFound
        serializer = BookDetailSerializer(book)
        return Response(serializer.data)