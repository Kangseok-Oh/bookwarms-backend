from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Review
from .serializers import reviewItemSerializer
from bookshelfs.models import BookshelfItem
from users.models import User
from books.models import Book

# 리뷰 리스트 API
class ReviewList(APIView):
    def get(self, request, book_isbn):
        # 해당 책에 등록된 리뷰 데이터 조회
        reviews = Review.objects.filter(review_book_isbn = book_isbn)
        
        # 있으면 json 변환 후 응답
        if reviews:
            serializer = reviewItemSerializer(reviews, many=True)
            return Response(serializer.data)
        
        # 없으면 오류
        else:
            raise NotFound

# 리뷰 작성 API
class submitReview(APIView):
    def post(self, request):
        # 리뷰 남긴 유저 이메일 추출
        user_email = request.user.user_email

        # 리뷰 데이터 파라미터에서 추출
        book_isbn = request.data.get('bookId')
        content = request.data.get('content')
        rating = request.data.get('rating')


        try:
            # 먼저 해당 책을 유저가 소유하고 있는지 확인
            bookshelf = BookshelfItem.objects.get(bookshelf_user_email = user_email, bookshelf_book_isbn = book_isbn)

            try:
                # 책 소유하고 있으면 리뷰를 썼는지 확인
                review = Review.objects.get(review_user_email = user_email, review_book_isbn = book_isbn)
                # 이미 썼으면 오류 응답
                return Response({"error": "이미 리뷰를 작성했습니다."})
            
            except Review.DoesNotExist:
                # 쓰지 않았으면 리뷰 등록
                user = User.objects.get(user_email = user_email)
                book = Book.objects.get(book_isbn = book_isbn)

                review = Review.objects.create(
                    review_user_email = user,
                    review_book_isbn = book,
                    review_content = content,
                    review_rating = rating
                )
                review.save()

                # ok 응답
                return Response({"ok": "리뷰 작성 완료"})

        except BookshelfItem.DoesNotExist:
            # 해당 책을 소유하고 있지 않으면 리뷰 쓸 수 없음
            return Response({"error": "보유하지 않은 책의 리뷰를 쓸 수 없습니다."})
        


