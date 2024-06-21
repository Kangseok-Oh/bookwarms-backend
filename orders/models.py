from django.db import models
from datetime import datetime

# 주문 모델
class Order(models.Model):
    # now = datetime.now()
    # str_time = now.strftime("%Y%m%d")

    # 컬럼들
    order_id = models.CharField(primary_key=True, max_length=16)
    order_user_email = models.ForeignKey("users.User", null=True, on_delete=models.SET_NULL)
    order_date = models.DateTimeField(auto_now_add=True)
    
    # 주문한 책 수
    def order_total_items(self):
        return self.orderitem_set.count()
    
    # 주문 총액
    def order_total_price(self):
        item_count = self.orderitem_set.count()
        if item_count == 0:
            return 0
        else:
            total_price = 0
            for book_price in self.orderitem_set.all().values("book__book_price"):
                total_price += book_price["book__book_price"]
            return total_price

# 주문한 책 아이템 모델
class OrderItem(models.Model):
    order_id = models.ForeignKey("orders.Order", on_delete=models.CASCADE)
    order_book_isbn = models.ForeignKey("books.Book", null=True, on_delete=models.SET_NULL) 

