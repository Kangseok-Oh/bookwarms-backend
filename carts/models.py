from django.db import models

# 장바구니 모델
class Cart(models.Model):
    # 컬럼
    cart_user_email = models.OneToOneField("users.User", primary_key=True ,on_delete=models.CASCADE)

    # 장바구니 내 책 개수
    def cart_total_items(self):
        return self.cartitem_set.count()
    
    # 장바구니 총액
    def cart_total_price(self):
        item_count = self.cartitem_set.count()
        if item_count == 0:
            return 0
        else:
            total_price = 0
            for book_price in self.cartitem_set.all().values("cart_book_isbn__book_price"):
                total_price += book_price["cart_book_isbn__book_price"]
            return total_price

# 장바구니 내 첵 모델
class CartItem(models.Model):
    cart_user_email = models.ForeignKey("carts.Cart", on_delete=models.CASCADE)
    cart_book_isbn = models.ForeignKey("books.Book", null=True, on_delete=models.SET_NULL)
