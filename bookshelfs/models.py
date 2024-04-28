from django.db import models

class Bookshelf(models.Model):
    bookshelf_user_email = models.OneToOneField("users.User", primary_key=True ,on_delete=models.CASCADE)

    def bookshelf_total_items(self):
        return self.bookshelfitem_set.count()

class BookshelfItem(models.Model):
    bookshelf_user_email = models.ForeignKey("bookshelfs.Bookshelf", on_delete=models.CASCADE)
    bookshelf_book_isbn = models.ForeignKey("books.Book", null=True, on_delete=models.SET_NULL)