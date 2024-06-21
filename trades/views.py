from datetime import datetime
from django.db.models import Count, Min, Max
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from .models import Trade, Sell as SellModel, Purchase as Pur
from .serializers import TradeChartSerializer, SellListSerializer, PurchaseListSerializer
from bookshelfs.models import BookshelfItem, Bookshelf
from books.models import Book
from users.models import User

# 거래 내역 조회 API
class TradeChart(APIView):
    def get(self, request, book_isbn):
        try:
            # 해당 책 isbn을 가진 책의 거래 데이터 조회
            trade = Trade.objects.filter(trade_book_isbn = book_isbn)
        except Trade.DoesNotExist:
            pass

        # 있으면 json 형식 변환 후 응답
        serializer = TradeChartSerializer(trade, many=True)
        return Response(serializer.data)
    
# 판매 입찰 내역 조회 API
class SellList(APIView):
    def get(self, request, book_isbn):
        # 해당 책 isbn을 가진 책의 판매 입찰 데이터를 판매 입찰가 기준으로 Group by해 조회
        sell = SellModel.objects.filter(sell_book_isbn = book_isbn).values('sell_price').annotate(count=Count('sell_price'))

        # 데이터 있으면 json 변환 후 응답
        if sell:
            serializer = SellListSerializer(sell, many=True)
            return Response(serializer.data)
        
        # 없으면 응답
        else:
            raise  NotFound
    
# 구매 입찰 내역 조회 API
class PurchaseList(APIView):
    def get(self, request, book_isbn):
        
        purchase = Pur.objects.filter(purchase_book_isbn = book_isbn).values('purchase_price').annotate(count=Count('purchase_price'))
        
        if purchase:
            serializer = PurchaseListSerializer(purchase, many=True)
            return Response(serializer.data)
        else:
            raise NotFound
        
# 즉시 구매가 조회 API
class ImmediateSellPrice(APIView):
    def get(self, request, book_isbn):
        try:
            # 해당 책의 판매 입찰가 중 가장 낮은 가격 조회
            sell = SellModel.objects.filter(sell_book_isbn = book_isbn).aggregate(sell_price = Min("sell_price"))
        except SellModel.DoesNotExist:
            # 없으면 오류
            raise NotFound
        
        # 있으면 응답
        return Response(sell)

# 즉시 판매가 조회 API 
class ImmediatePurPrice(APIView):
    def get(self, request, book_isbn):
        try:
            # 해당 책의 구매 입찰가 중 가장 높은 가격 조회
            purchase = Pur.objects.filter(purchase_book_isbn = book_isbn).aggregate(purchase_price = Max("purchase_price"))
        except Pur.DoesNotExist:
            raise NotFound
        return Response(purchase)

# 판매 입찰 API    
class Sell(APIView):
    # 로그인 시에만 호출 가능
    permission_classes = [IsAuthenticated]
    def post(self, request):
        # 입찰한 유저 이메일 추출
        sell_user_email = request.user.user_email

        # 파라미터에서 책 isbn, 판매 입찰가 추출
        sell_book_isbn = request.data.get('sell_book_isbn')
        sell_price = request.data.get('sell_price')

        try:
            # 해당 책을 유저가 소유하고 있는지 확인
            bookshelf = BookshelfItem.objects.get(bookshelf_user_email = sell_user_email, bookshelf_book_isbn = sell_book_isbn)
            try:
                # 소유하고 있으면 이미 해당 책을 판매 입찰 했는지 확인
                sell = SellModel.objects.get(sell_seller_email = sell_user_email, sell_book_isbn = sell_book_isbn)
                # 이미 입찰했으면 오류 응답
                return Response({"error": "이미 판매 입찰 등록한 책입니다."})
            except:
                # 입찰하지 않았으면 입찰 데이터 추가
                user = User.objects.get(user_email = sell_user_email)
                book = Book.objects.get(book_isbn = sell_book_isbn)

                sell = SellModel.objects.create(
                    sell_seller_email = user,
                    sell_price = sell_price,
                    sell_book_isbn = book
                )
                sell.save()

                # ok 응답
                return Response({"ok": "판매 입찰되었습니다."})


        except BookshelfItem.DoesNotExist:
            # 소유하고 있지 않으면 오류 응답
            return Response({"error": "현재 보유하고 있는 책이 아닙니다."})
        
# 즉시 판매 API
class ImmediateSell(APIView):
    permission_classes = [IsAuthenticated]

    # 거래 번호 부여 메소드
    def getNewId(self):
        # 현재 날짜 8자리(YYYYMMDD) 형식으로 추출
        now = datetime.now()
        str_time = now.strftime("%Y%m%d")
        
        # 금일 마지막 거래 조회
        final_trade = Trade.objects.filter(trade_id__startswith = str_time)

        # 만약 마지막 거래 데이터가 있으면
        if final_trade:
            # 마지막 거래 번호 추출
            final_trade_id = final_trade.aggregate(trade_id = Max('trade_id'))
            # 그 다음 번호로 거래 번호로 지정
            id = str(int(final_trade_id.get("trade_id")) + 1)
        else:
            # 없으면 1번으로 지정
            id = str_time + format(1, '08')
        # 거래 번호 반환
        return id
    
    def post(self, request):
        # 요청한 유저 이메일 추출
        user_email = request.user.user_email
        # 파라미터에서 책 isbn, 거래가 추출
        book_isbn = request.data.get('trade_book_isbn')
        price = request.data.get('trade_price')

        try:
            # 해당 책을 유저가 소유하고 있는지 확인
            bookshelf = BookshelfItem.objects.get(bookshelf_user_email = user_email, bookshelf_book_isbn = book_isbn)
            try:
                # 소유중이면 해당 책이 판매 입찰 중인지 확인
                sell = SellModel.objects.get(sell_seller_email = user_email, sell_book_isbn = book_isbn)
                # 이미 입찰 중이면 오류 응답
                return Response({"error": "이미 판매 등록중인 책입니다."})
            except:
                # 입찰 중이 아니면
                # 판매자 데이터 조회
                user = User.objects.get(user_email = user_email)

                # 최고 가격에 구매 입찰한 입찰 데이터 및 구매자 조회
                purchase = Pur.objects.get(purchase_price = price, purchase_book_isbn = book_isbn)
                buyer_email = purchase.purchase_buyer_email.user_email
                buyer = User.objects.get(user_email = buyer_email)

                book = Book.objects.get(book_isbn = book_isbn)

                # 거래 데이터 추가
                sell = Trade.objects.create(
                    trade_id = self.getNewId(),
                    trade_seller_email = user,
                    trade_buyer_email = buyer,
                    trade_book_isbn = book,
                    trade_price = price,
                )
                sell.save()

                # 응찰된 판매 입찰 데이터 삭제
                purchase.delete()

                # 구매자의 내 서재에 책 데이터 추가 
                buyer_bookshelf = Bookshelf.objects.get(bookshelf_user_email = buyer_email)
                buyer_bookshelf_item = BookshelfItem.objects.create(
                    bookshelf_user_email = buyer_bookshelf,
                    bookshelf_book_isbn = book
                )
                buyer_bookshelf_item.save()

                # 유저의 내 서재에서 책 데이터 삭제
                seller_bookshelf_item = BookshelfItem.objects.get(bookshelf_user_email = user_email, bookshelf_book_isbn = book_isbn)
                seller_bookshelf_item.delete()

                # 유저의 잔액에서 거래가만큼 더하기
                user_cash = user.user_cash
                user_cash += price
                user.user_cash = user_cash
                user.save()

                # 구매자의 잔액에서 거래가만큼 빼기
                buyer_cash = buyer.user_cash
                buyer_cash -= price
                buyer.user_cash = buyer_cash
                buyer.save()

                # ok 응답
                return Response({"ok": "판매 완료"})

        except BookshelfItem.DoesNotExist:
            # 보유하고 있지 않으면 오류
            return Response({"error": "현재 보유하고 있는 책이 아닙니다."})
        
# 구매 입찰 API
class Purchase(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        # 요청한 유저 이메일 추출
        purchase_user_email = request.user.user_email
        # 파라미터에서 책 isbn, 거래가 추출
        purchase_book_isbn = request.data.get('purchase_book_isbn')
        purchase_price = request.data.get('purchase_price')

        try:
            # 해당 책을 보유하고 있는지 확인
            bookshelf = BookshelfItem.objects.get(bookshelf_user_email = purchase_user_email, bookshelf_book_isbn = purchase_book_isbn)
            # 보유중이면 오류 응답
            return Response({"error": "이미 보유하고 있는 책입니다."})
        except BookshelfItem.DoesNotExist:
            # 보유중이 아니면
            try:
                # 이미 구매 입찰을 했는지 확인
                purchase = Pur.objects.get(purchase_buyer_email = purchase_user_email, purchase_book_isbn = purchase_book_isbn)
                # 입찰했으면 오류 응답
                return Response({"error": "이미 구매 입찰 등록한 책입니다."})
            except:
                # 입찰하지 않았으면 구매 입찰 데이터 추가
                user = User.objects.get(user_email = purchase_user_email)
                book = Book.objects.get(book_isbn = purchase_book_isbn)

                purchase = Pur.objects.create(
                    purchase_buyer_email = user,
                    purchase_price = purchase_price,
                    purchase_book_isbn = book
                )
                purchase.save()

                # ok 응답
                return Response({"ok": "구매 입찰되었습니다."})

# 즉시 구매 API           
class ImmediatePurchase(APIView):
    permission_classes = [IsAuthenticated]
    def getNewId(self):
        now = datetime.now()
        str_time = now.strftime("%Y%m%d")
        
        final_trade = Trade.objects.filter(trade_id__startswith = str_time)

        if final_trade:
            final_trade_id = final_trade.aggregate(trade_id = Max('trade_id'))
            id = str(int(final_trade_id.get("trade_id")) + 1)
        else:
            id = str_time + format(1, '08')

        return id
    
    def post(self, request):
        # 요청한 유저 이메일 추출
        user_email = request.user.user_email
        # 파라미터에서 책 isbn, 거래가 추출
        book_isbn = request.data.get('trade_book_isbn')
        price = request.data.get('trade_price')

        try:
            # 이미 책을 보유중인지 확인
            bookshelf = BookshelfItem.objects.get(bookshelf_user_email = user_email, bookshelf_book_isbn = book_isbn)
            # 보유 중이면 오류 응답
            return Response({"error": "이미 보유하고 있는 책입니다."})
        except BookshelfItem.DoesNotExist:
            try:
                # 보유하고 있지 않으면 이미 구매 입찰중인지 확인
                purchase = Pur.objects.get(purchase_buyer_email = user_email, purchase_book_isbn = book_isbn)
                # 입찰중이면 오류 응답
                return Response({"error": "이미 구매 입찰 등록한 책입니다."})
            except Pur.DoesNotExist:
                # 입찰하지 않았으면
                # 유저 데이터 조회
                user = User.objects.get(user_email = user_email)

                # 최저가에 판매 입찰 등록한 입찰 데이터 및 판매자 데이터 조회
                sell = SellModel.objects.get(sell_price = price, sell_book_isbn = book_isbn)
                seller_email = sell.sell_seller_email.user_email
                seller = User.objects.get(user_email = seller_email)

                book = Book.objects.get(book_isbn = book_isbn)

                # 거래 데이터 생성
                purchase = Trade.objects.create(
                    trade_id = self.getNewId(),
                    trade_seller_email = seller,
                    trade_buyer_email = user,
                    trade_book_isbn = book,
                    trade_price = price,
                )
                purchase.save()

                # 응찰된 판매 입찰 데이터 삭제
                sell.delete()

                # 유저의 내 서재에 책 데이터 추가
                user_bookshelf = Bookshelf.objects.get(bookshelf_user_email = user_email)
                user_bookshelf_item = BookshelfItem.objects.create(
                    bookshelf_user_email = user_bookshelf,
                    bookshelf_book_isbn = book
                )
                user_bookshelf_item.save()

                # 판매자의 내 서재에서 책 데이터 삭제
                seller_bookshelf_item = BookshelfItem.objects.get(bookshelf_user_email = seller_email, bookshelf_book_isbn = book_isbn)
                seller_bookshelf_item.delete()

                # 유저의 잔액에서 거래가만큼 빼기
                user_cash = user.user_cash
                user_cash -= price
                user.user_cash = user_cash
                user.save()

                # 판매자의 잔액에서 거래가만큼 더하기
                seller_cash = seller.user_cash
                seller_cash += price
                seller.user_cash = seller_cash
                seller.save()

                # ok 응답
                return Response({"ok": "구매 완료"})


            

        