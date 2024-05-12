from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Book

class CategoryBookListSerializer(ModelSerializer):
    book_rating = SerializerMethodField()
    book_author_name = SerializerMethodField()
    book_review_count = SerializerMethodField()
    class Meta:
        model = Book
        fields = (
            "book_isbn",
            "book_cover_path",
            "book_name",
            "book_rating",
            "book_review_count",
            "book_price",
            "book_author_name",
        )
    
    def get_book_author_name(self, book):
        return book.book_author_id.author_name
    
    def get_book_rating(self, book):
        return book.book_rating()
    
    def get_book_review_count(self, book):
        return book.book_review_count()
    
class BookDetailSerializer(ModelSerializer):
    book_rating = SerializerMethodField()
    book_author_name = SerializerMethodField()
    book_author_intro = SerializerMethodField()
    book_review_count = SerializerMethodField()

    class Meta:
        model = Book
        fields = (
            "book_isbn",
            "book_cover_path",
            "book_name",
            "book_rating",
            "book_review_count",
            "book_price",
            "book_author_name",
            "book_publisher",
            "book_interpreter",
            "book_intro",
            "book_contents",
            "book_author_intro"
        )

    def get_book_rating(self, book):
        return book.book_rating()
    
    def get_book_author_name(self, book):
        return book.book_author_id.author_name
    
    def get_book_author_intro(self, book):
        return book.book_author_id.author_intro
    
    def get_book_review_count(self, book):
        return book.book_review_count()

class BookShelfBookSerializer(ModelSerializer):
    book_author_name = SerializerMethodField()
    book_rating = SerializerMethodField()

    class Meta:
        model = Book
        fields = (
            "book_isbn",
            "book_cover_path",
            "book_name",
            "book_rating",
            "book_author_name"
        )
    
    def get_book_rating(self, book):
        return book.book_rating()
    
    def get_book_author_name(self, book):
        return book.book_author_id.author_name