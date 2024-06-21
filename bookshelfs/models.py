from django.db import models

# 내 서재 모델
class Bookshelf(models.Model):
    # 컬럼
    bookshelf_user_email = models.OneToOneField("users.User", primary_key=True ,on_delete=models.CASCADE)

    # 내 서재의 책 개수
    def bookshelf_total_items(self):
        return self.bookshelfitem_set.count()

# 내 서재 내의 책 아이템 모델
class BookshelfItem(models.Model):
    # 컬럼들
    bookshelf_user_email = models.ForeignKey("bookshelfs.Bookshelf", on_delete=models.CASCADE)
    bookshelf_book_isbn = models.ForeignKey("books.Book", null=True, on_delete=models.SET_NULL)