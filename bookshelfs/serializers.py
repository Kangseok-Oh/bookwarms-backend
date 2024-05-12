from rest_framework.serializers import ModelSerializer
from .models import Bookshelf, BookshelfItem
from books.serializers import BookShelfBookSerializer

class BookshelfListSerializer(ModelSerializer):
    bookshelf_book_isbn = BookShelfBookSerializer(read_only=True)

    class Meta:
        model = BookshelfItem
        fields = (
            "bookshelf_book_isbn",
        )