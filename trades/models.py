from django.db import models

# 거래 모델
class Trade(models.Model):
    trade_id = models.CharField(max_length=16, primary_key=True)
    trade_seller_email = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, related_name='trade_sold')
    trade_buyer_email = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, related_name='trade_purchased')
    trade_book_isbn = models.ForeignKey("books.Book", on_delete=models.SET_NULL, null=True)
    trade_price = models.IntegerField()
    trade_date = models.DateField(auto_now_add=True)

# 판매 입찰 모델
class Sell(models.Model):
    sell_seller_email = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    sell_book_isbn = models.ForeignKey("books.Book", on_delete=models.SET_NULL, null=True)
    sell_price = models.IntegerField()

# 구매 입찰 모델
class Purchase(models.Model):
    purchase_buyer_email = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    purchase_book_isbn = models.ForeignKey("books.Book", on_delete=models.SET_NULL, null=True)
    purchase_price = models.IntegerField()

