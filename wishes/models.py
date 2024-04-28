from django.db import models

class Wish(models.Model):
    wish_user_email = models.OneToOneField("users.User", primary_key=True ,on_delete=models.CASCADE)

    def wish_total_items(self):
        return self.wishitem_set.count()

class WishItem(models.Model):
    wish_user_email = models.ForeignKey("wishes.Wish", on_delete=models.CASCADE)
    wish_book_isbn = models.ForeignKey("books.Book", null=True, on_delete=models.SET_NULL)

