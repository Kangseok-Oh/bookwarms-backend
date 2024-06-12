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

class TradeChart(APIView):
    def get(self, request, book_isbn):
        try:
            trade = Trade.objects.filter(trade_book_isbn = book_isbn)
        except Trade.DoesNotExist:
            pass
        serializer = TradeChartSerializer(trade, many=True)
        return Response(serializer.data)
    
class SellList(APIView):
    def get(self, request, book_isbn):
        sell = SellModel.objects.filter(sell_book_isbn = book_isbn).values('sell_price').annotate(count=Count('sell_price'))

        if sell:
            serializer = SellListSerializer(sell, many=True)
            return Response(serializer.data)
        else:
            raise  NotFound
    
class PurchaseList(APIView):
    def get(self, request, book_isbn):
        try:
            purchase = Pur.objects.filter(purchase_book_isbn = book_isbn).values('purchase_price').annotate(count=Count('purchase_price'))
        except Pur.DoesNotExist:
            pass
        serializer = PurchaseListSerializer(purchase, many=True)
        return Response(serializer.data)
        
class ImmediateSellPrice(APIView):
    def get(self, request, book_isbn):
        try:
            sell = SellModel.objects.filter(sell_book_isbn = book_isbn).aggregate(sell_price = Min("sell_price"))
        except SellModel.DoesNotExist:
            raise NotFound
        return Response(sell)
    
class ImmediatePurPrice(APIView):
    def get(self, request, book_isbn):
        try:
            purchase = Pur.objects.filter(purchase_book_isbn = book_isbn).aggregate(purchase_price = Max("purchase_price"))
        except Pur.DoesNotExist:
            raise NotFound
        return Response(purchase)
        
class Sell(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        sell_user_email = request.user.user_email
        sell_book_isbn = request.data.get('sell_book_isbn')
        sell_price = request.data.get('sell_price')

        try:
            bookshelf = BookshelfItem.objects.get(bookshelf_user_email = sell_user_email, bookshelf_book_isbn = sell_book_isbn)
            try:
                sell = SellModel.objects.get(sell_seller_email = sell_user_email, sell_book_isbn = sell_book_isbn)
                return Response({"error": "이미 판매 등록중인 책입니다."})
            except:
                user = User.objects.get(user_email = sell_user_email)
                book = Book.objects.get(book_isbn = sell_book_isbn)

                sell = SellModel.objects.create(
                    sell_seller_email = user,
                    sell_price = sell_price,
                    sell_book_isbn = book
                )
                sell.save()
                return Response({"ok": "판매 입찰되었습니다."})


        except BookshelfItem.DoesNotExist:
            return Response({"error": "현재 보유하고 있는 책이 아닙니다."})
        
class ImmediateSell(APIView):
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
        user_email = request.user.user_email
        book_isbn = request.data.get('trade_book_isbn')
        price = request.data.get('trade_price')

        try:
            bookshelf = BookshelfItem.objects.get(bookshelf_user_email = user_email, bookshelf_book_isbn = book_isbn)
            try:
                sell = SellModel.objects.get(sell_seller_email = user_email, sell_book_isbn = book_isbn)
                return Response({"error": "이미 판매 등록중인 책입니다."})
            except:
                user = User.objects.get(user_email = user_email)
                purchase = Pur.objects.get(purchase_price = price, purchase_book_isbn = book_isbn)
                
                buyer_email = purchase.purchase_buyer_email.user_email
                buyer = User.objects.get(user_email = buyer_email)

                book = Book.objects.get(book_isbn = book_isbn)

                sell = Trade.objects.create(
                    trade_id = self.getNewId(),
                    trade_seller_email = user,
                    trade_buyer_email = buyer,
                    trade_book_isbn = book,
                    trade_price = price,
                )
                sell.save()
                purchase.delete()

                buyer_bookshelf = Bookshelf.objects.get(bookshelf_user_email = buyer_email)

                buyer_bookshelf_item = BookshelfItem.objects.create(
                    bookshelf_user_email = buyer_bookshelf,
                    bookshelf_book_isbn = book
                )
                buyer_bookshelf_item.save()

                seller_bookshelf_item = BookshelfItem.objects.get(bookshelf_user_email = user_email, bookshelf_book_isbn = book_isbn)
                seller_bookshelf_item.delete()

                user_cash = user.user_cash
                user_cash += price
                user.user_cash = user_cash
                user.save()

                buyer_cash = buyer.user_cash
                buyer_cash -= price
                buyer.user_cash = buyer_cash
                buyer.save()

                return Response({"ok": "판매 완료"})

        except BookshelfItem.DoesNotExist:
            return Response({"error": "현재 보유하고 있는 책이 아닙니다."})
        
class Purchase(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        purchase_user_email = request.user.user_email
        purchase_book_isbn = request.data.get('purchase_book_isbn')
        purchase_price = request.data.get('purchase_price')

        try:
            bookshelf = BookshelfItem.objects.get(bookshelf_user_email = purchase_user_email, bookshelf_book_isbn = purchase_book_isbn)
            return Response({"error": "이미 보유하고 있는 책입니다."})
        except BookshelfItem.DoesNotExist:
            try:
                purchase = Pur.objects.get(purchase_buyer_email = purchase_user_email, purchase_book_isbn = purchase_book_isbn)
                return Response({"error": "이미 구매 등록중인 책입니다."})
            except:
                user = User.objects.get(user_email = purchase_user_email)
                book = Book.objects.get(book_isbn = purchase_book_isbn)

                purchase = Pur.objects.create(
                    purchase_buyer_email = user,
                    purchase_price = purchase_price,
                    purchase_book_isbn = book
                )
                purchase.save()
                return Response({"ok": "구매 입찰되었습니다."})
            
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
        user_email = request.user.user_email
        book_isbn = request.data.get('trade_book_isbn')
        price = request.data.get('trade_price')

        try:
            bookshelf = BookshelfItem.objects.get(bookshelf_user_email = user_email, bookshelf_book_isbn = book_isbn)
            return Response({"error": "이미 보유하고 있는 책입니다."})
        except BookshelfItem.DoesNotExist:
            try:
                purchase = Pur.objects.get(purchase_buyer_email = user_email, purchase_book_isbn = book_isbn)
                return Response({"error": "이미 구매 등록중인 책입니다."})
            except Pur.DoesNotExist:
                user = User.objects.get(user_email = user_email)
                sell = SellModel.objects.get(sell_price = price, sell_book_isbn = book_isbn)
                
                seller_email = sell.sell_seller_email.user_email
                seller = User.objects.get(user_email = seller_email)

                book = Book.objects.get(book_isbn = book_isbn)

                purchase = Trade.objects.create(
                    trade_id = self.getNewId(),
                    trade_seller_email = seller,
                    trade_buyer_email = user,
                    trade_book_isbn = book,
                    trade_price = price,
                )
                purchase.save()
                sell.delete()

                user_bookshelf = Bookshelf.objects.get(bookshelf_user_email = user_email)

                user_bookshelf_item = BookshelfItem.objects.create(
                    bookshelf_user_email = user_bookshelf,
                    bookshelf_book_isbn = book
                )
                user_bookshelf_item.save()

                seller_bookshelf_item = BookshelfItem.objects.get(bookshelf_user_email = seller_email, bookshelf_book_isbn = book_isbn)
                seller_bookshelf_item.delete()

                user_cash = user.user_cash
                user_cash -= price
                user.user_cash = user_cash
                user.save()

                seller_cash = seller.user_cash
                seller_cash += price
                seller.user_cash = seller_cash
                seller.save()

                return Response({"ok": "구매 완료"})


            

        