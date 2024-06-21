from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from books.models import Book
from bookshelfs.models import BookshelfItem
from .models import Cart, CartItem
from .serializers import CartListSerializer

# 장바구니 내 책 리스트 API
class CartList(APIView):
    # 로그인 시에만 호출 가능
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # 요청한 유저 이메일 추출
        user_email = request.user.user_email
        try:
            # 해당 유저의 장바구니 데이터 조회
            cart_list = Cart.objects.get(cart_user_email = user_email)
        except:
            # 없으면 오류
            raise NotFound
        # json 변환 후 응답
        serializer = CartListSerializer(cart_list)
        return Response(serializer.data)
    
# 장바구니에 책 추가 API
class AddCart(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        # 요청한 유저 이메일과 책 isbn 추출
        user_email = request.user.user_email
        book_isbn = request.data.get('book_isbn')
        
        try:
            # 해당 책을 이미 유저가 소유하고 있는지 조회
            bookshelf = BookshelfItem.objects.get(bookshelf_user_email = user_email, bookshelf_book_isbn = book_isbn)
            # 소유하고 있으면 오류 응답
            return Response({"error": "이미 구매한 책입니다."})
        
        except BookshelfItem.DoesNotExist:
            # 해당 책을 소유하고 있지 않으면
            try:
                # 이미 해당 책이 장바구니에 담겼는지 조회
                cart_item = CartItem.objects.get(cart_user_email = user_email, cart_book_isbn = book_isbn)
                # 담겨 있으면 오류 응답
                return Response({"error": "이미 장바구니에 담긴 책입니다."})
            except CartItem.DoesNotExist:
                # 만약 담겨 있지 않으면

                cart = Cart.objects.get(cart_user_email = user_email)
                book = Book.objects.get(book_isbn = book_isbn)

                # 장바구니 데이터에 해당 책 데이터 추가 
                cart_item = CartItem.objects.create(
                    cart_user_email = cart,
                    cart_book_isbn = book
                )
                cart_item.save()

                # ok 응답
                return Response({"ok": "장바구니에 추가되었습니다."})

# 장바구니 내 책 삭제 API 
class DeleteCart(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request):
        # 요청 보낸 유저 이메일과 책 isbn 추출
        user_email = request.user.user_email
        book_isbn = request.data.get('book_isbn')

        # 해당 유저의 장바구니에 해당 책 조회
        cart_item = CartItem.objects.filter(cart_user_email = user_email, cart_book_isbn__in = book_isbn)

        # 삭제 후 ok 응답
        cart_item.delete()
        return Response({"ok": "삭제 완료"})