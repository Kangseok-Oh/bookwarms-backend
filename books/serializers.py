from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Book
from authors.serializers import AuthorSerializer
from categories.serializers import CategorySerializer

class CategoryBookListSerializer(ModelSerializer):
    book_rating = SerializerMethodField()
    book_author_name = SerializerMethodField()
    class Meta:
        model = Book
        fields = (
            "book_isbn",
            "book_cover_path",
            "book_name",
            "book_rating",
            "book_price",
            "book_author_name",
        )
    
    def get_book_author_name(self, book):
        return book.book_author_id.author_name
    
    def get_book_rating(self, book):
        return book.book_rating()
