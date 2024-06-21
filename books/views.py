from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Book
from .serializers import BookDetailSerializer, CategoryBookListSerializer, CartBookSerializer

# 카테고리 별 책 리스트 API
class CategoryBookList(APIView):
    def get(self, request, category_id):
        try:
            # 해당 카테고리 id를 가지고 있는 책 데이터 조회
            books = Book.objects.filter(book_category_id = category_id)
        except:
            # 없으면 오류
            raise NotFound
        # json 형식으로 변환 후 응답
        serializer = CategoryBookListSerializer(books, many=True)
        return Response(serializer.data)

# 책 상세 페이지 데이터 API 
class BookDetail(APIView):
    def get(self, request, book_isbn):
        try:
            # 해당 책 isbn 가지고 있는 책 데이터 조회
            book = Book.objects.get(book_isbn = book_isbn)
        except:
            # 없으면 오류
            raise NotFound
        # json 형식으로 변환 후 응답
        serializer = BookDetailSerializer(book)
        return Response(serializer.data)
    
# 거래할 책 데이터 API
class TradeBook(APIView):
    def get(self, request, book_isbn):
        try:
            # 해당 책 isbn 가지고 있는 책 데이터 조회
            book = Book.objects.get(book_isbn = book_isbn)
        except:
            # 없으면 오류
            raise NotFound
        # json 형식으로 변환 후 응답
        serializer = CartBookSerializer(book)
        return Response(serializer.data)
    
# 책 검색 API
class SearchList(APIView):
    def get(self, request, key_word):
        # 검색어를 책 이름에 포함하는 책 데이터 조회
        books = Book.objects.filter(book_name__contains = key_word)

        if books:
            # 있으면 json 형식으로 변환 후 응답
            serializer = CategoryBookListSerializer(books, many=True)
            return Response(serializer.data)
        else:
            # 없으면 오류
            raise NotFound

    