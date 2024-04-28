from django.db import models
from datetime import datetime

class Order(models.Model):
    now = datetime.now()
    str_time = now.strftime("%Y%m%d")

    order_id = models.CharField(primary_key=True, max_length=16)
    order_user_email = models.ForeignKey("users.User", null=True, on_delete=models.SET_NULL)
    order_date = models.DateTimeField(auto_now_add=True)
    
    def order_total_items(self):
        return self.orderitem_set.count()
    
    def order_total_price(self):
        item_count = self.orderitem_set.count()
        if item_count == 0:
            return 0
        else:
            total_price = 0
            for book_price in self.orderitem_set.all().values("book__book_price"):
                total_price += book_price["book__book_price"]
            return total_price

class OrderItem(models.Model):
    order_id = models.ForeignKey("orders.Order", on_delete=models.CASCADE)
    order_book_isbn = models.ForeignKey("books.Book", null=True, on_delete=models.SET_NULL) 

