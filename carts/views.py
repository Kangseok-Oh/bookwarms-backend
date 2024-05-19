from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from books.models import Book
from .models import Cart, CartItem
from .serializers import CartListSerializer

class CartList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user_email = request.user.user_email
        try:
            cart_list = Cart.objects.get(cart_user_email = user_email)
        except:
            raise NotFound
        serializer = CartListSerializer(cart_list)
        return Response(serializer.data)
    
class AddCart(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user_email = request.user.user_email
        book_isbn = request.data.get('book_isbn')
        try:
            cart_item = CartItem.objects.get(cart_user_email = user_email, cart_book_isbn = book_isbn)
            return Response({"error": "이미 장바구니에 담긴 책입니다."})
        except CartItem.DoesNotExist:
            cart = Cart.objects.get(cart_user_email = user_email)
            book = Book.objects.get(book_isbn = book_isbn)

            cart_item = CartItem.objects.create(
                cart_user_email = cart,
                cart_book_isbn = book
            )
            cart_item.save()
            return Response({"ok": "장바구니에 추가되었습니다."})
        
class DeleteCart(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request):
        user_email = request.user.user_email
        book_isbn = request.data.get('book_isbn')

        cart_item = CartItem.objects.filter(cart_user_email = user_email, cart_book_isbn__in = book_isbn)
        cart_item.delete()
        return Response({"ok": "삭제 완료"})