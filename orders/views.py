from django.db.models import Max
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from bookshelfs.models import BookshelfItem, Bookshelf
from users.models import User
from books.models import Book
from books.serializers import CartBookSerializer
from .models import Order as OrderModel, OrderItem

# 주문할 책 리스트 API
class OrderList(APIView):
    # 로그인 시에만 호출 가능
    permission_classes = [IsAuthenticated]
    def post(self, request):
        # 파라미터에서 책 isbn 추출
        book_isbn = request.data.get('book_isbn')
        try:
            # 해당 책 데이터 조회
            books = Book.objects.filter(book_isbn__in = book_isbn)

            # 있으면 json 형식 변환 후 응답
            serializer = CartBookSerializer(books, many=True)
            return Response(serializer.data)
        
        except Book.DoesNotExist:
            # 없으면 오류
            raise NotFound
        
# 주문 API        
class Order(APIView):
    permission_classes = [IsAuthenticated]

    # 주문번호 부여 메소드
    def getNewId(self):
        # 현재 날짜 8자리(YYYYMMDD) 형식으로 추출
        now = datetime.now()
        str_time = now.strftime("%Y%m%d")
        
        # 금일 마지막 주문 조회
        final_order = OrderModel.objects.filter(order_id__startswith = str_time)

        # 만약 마지막 주문 데이터가 있으면
        if final_order:
            # 마지막 주문번호 추출
            final_order_id = final_order.aggregate(order_id = Max('order_id'))
            # 그 다음 번호를 주문번호 지정
            id = str(int(final_order_id.get("order_id")) + 1)

        # 없으면 1번으로 지정
        else:
            id = str_time + format(1, '08')

        # 주문번호 반환
        return id

    def post(self, request):
        # 요청 보낸 유저 이메일, 주문하는 책 isbn 추출
        user_email = request.user.user_email
        book_isbn = request.data.get('book_isbn')

        # 유저 데이터 조회
        user = User.objects.get(user_email = user_email)

        # 주문 총액 계산
        total_price = 0
        for book in Book.objects.filter(book_isbn__in = book_isbn):
            total_price += book.book_price

        # 만약 잔액이 부족하면 잔액 부족 오류 응답
        if user.user_cash < total_price:
            return Response({"error": f"잔액이 부족합니다!"})
        
        # 잔액이 충분하면
        else:
                # 주문 데이터 생성
                order = OrderModel.objects.create(
                    order_id = self.getNewId(),
                    order_user_email = user,
                )
                order.save()

                # 주문한 유저의 내 서재 데이터 조회
                bookshelf = Bookshelf.objects.get(bookshelf_user_email = user_email)

                # 주문한 책들 데이터 내 서재 데이터에 추가
                for book in Book.objects.filter(book_isbn__in = book_isbn):
                    order_item = OrderItem.objects.create(
                        order_id = order,
                        order_book_isbn = book
                    )
                    order_item.save()

                    bookshelf_item = BookshelfItem.objects.create(
                        bookshelf_user_email = bookshelf,
                        bookshelf_book_isbn = book
                    )
                
                # 유저의 잔액에서 주문 금액 빼기
                cash = user.user_cash
                cash -= total_price
                user.user_cash = cash
                user.save()

                # ok 응답
                return Response({"ok": "ok"})



            

        
