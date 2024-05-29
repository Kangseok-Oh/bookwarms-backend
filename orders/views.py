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

class OrderList(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        book_isbn = request.data.get('book_isbn')
        try:
            books = Book.objects.filter(book_isbn__in = book_isbn)
            serializer = CartBookSerializer(books, many=True)
            return Response(serializer.data)
        except Book.DoesNotExist:
            raise NotFound
        
class Order(APIView):
    permission_classes = [IsAuthenticated]

    def getNewId(self):
        now = datetime.now()
        str_time = now.strftime("%Y%m%d")
        # id = str_time + format(Order.sequence, '08')
        try:
            final_order = OrderModel.objects.filter(order_id__startswith = str_time)
            final_order_id = final_order.aggregate(order_id = Max('order_id'))
            id = str(int(final_order_id.get("order_id")) + 1)
        except OrderModel.DoesNotExist:
            id = str_time + format(1, '08')

        return id

    def post(self, request):
        user_email = request.user.user_email
        book_isbn = request.data.get('book_isbn')

        user = User.objects.get(user_email = user_email)

        total_price = 0
        for book in Book.objects.filter(book_isbn__in = book_isbn):
            total_price += book.book_price

        if user.user_cash < total_price:
            return Response({"error": f"잔액이 부족합니다!"})
        else:
                order = OrderModel.objects.create(
                    order_id = self.getNewId(),
                    order_user_email = user,
                )
                order.save()

                bookshelf = Bookshelf.objects.get(bookshelf_user_email = user_email)

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
                
                cash = user.user_cash
                cash -= total_price
                user.user_cash = cash
                user.save()
                return Response({"ok": "ok"})



            

        
