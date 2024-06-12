from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Review
from .serializers import reviewItemSerializer
from bookshelfs.models import BookshelfItem
from users.models import User
from books.models import Book

class ReviewList(APIView):
    def get(self, request, book_isbn):
        reviews = Review.objects.filter(review_book_isbn = book_isbn)
        
        if reviews:
            serializer = reviewItemSerializer(reviews, many=True)
            return Response(serializer.data)
        else:
            raise NotFound
        
class submitReview(APIView):
    def post(self, request):
        user_email = request.user.user_email
        book_isbn = request.data.get('bookId')
        content = request.data.get('content')
        rating = request.data.get('rating')

        try:
            bookshelf = BookshelfItem.objects.get(bookshelf_user_email = user_email, bookshelf_book_isbn = book_isbn)
            try:
                review = Review.objects.get(review_user_email = user_email, review_book_isbn = book_isbn)
                return Response({"error": "이미 리뷰를 작성했습니다."})
            except Review.DoesNotExist:
                user = User.objects.get(user_email = user_email)
                book = Book.objects.get(book_isbn = book_isbn)

                review = Review.objects.create(
                    review_user_email = user,
                    review_book_isbn = book,
                    review_content = content,
                    review_rating = rating
                )
                review.save()

                return Response({"ok": "리뷰 작성 완료"})

        except BookshelfItem.DoesNotExist:
            return Response({"error": "보유하지 않은 책의 리뷰를 쓸 수 없습니다."})
        


