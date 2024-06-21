from rest_framework.serializers import ModelSerializer
from .models import Bookshelf, BookshelfItem
from books.serializers import BookShelfBookSerializer

# 내 서재 책 리스트용 json 데이터 형식 지정
class BookshelfListSerializer(ModelSerializer):
    # 책 isbn으로 책 json 데이터 가져오기
    bookshelf_book_isbn = BookShelfBookSerializer(read_only=True)

    class Meta:
        model = BookshelfItem
        fields = (
            "bookshelf_book_isbn",
        )