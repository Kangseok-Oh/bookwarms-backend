from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Book

# 카테고리 별 책 리스트용 책 데이터 json 형식 지정
class CategoryBookListSerializer(ModelSerializer):
    book_rating = SerializerMethodField()
    book_author_name = SerializerMethodField()
    book_review_count = SerializerMethodField()
    class Meta:
        model = Book
        # 컬럼들
        fields = (
            "book_isbn",
            "book_cover_path",
            "book_name",
            "book_rating",
            "book_review_count",
            "book_price",
            "book_author_name",
        )
    
    # 작가 이름
    def get_book_author_name(self, book):
        return book.book_author_id.author_name
    
    # 책 평점
    def get_book_rating(self, book):
        return book.book_rating()
    
    # 책 리뷰 수
    def get_book_review_count(self, book):
        return book.book_review_count()
    
# 책 상세 페이지용 책 데이터 json 형식 지정 
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
            "book_author_intro",
            "book_ebook_path"
        )

    # 책 평점
    def get_book_rating(self, book):
        return book.book_rating()
    
    # 작가 이름
    def get_book_author_name(self, book):
        return book.book_author_id.author_name
    
    # 작가 소개
    def get_book_author_intro(self, book):
        return book.book_author_id.author_intro
    
    # 리뷰 수
    def get_book_review_count(self, book):
        return book.book_review_count()

# 내 서재 책 리스트용 책 데이터 json 형식 지정
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
    

# 장바구니 책 리스트용 책 데이터 json 형식 지정
class CartBookSerializer(ModelSerializer):
    book_author_name = SerializerMethodField()

    class Meta:
        model = Book
        fields = (
            "book_isbn",
            "book_cover_path",
            "book_name",
            "book_price",
            "book_author_name"
        )

    def get_book_author_name(self, book):
        return book.book_author_id.author_name