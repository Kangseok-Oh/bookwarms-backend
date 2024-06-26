from django.db import models

# 리뷰 모델
class Review(models.Model):
    # 컬럼들
    review_user_email = models.ForeignKey("users.User", on_delete=models.CASCADE)
    review_book_isbn = models.ForeignKey("books.Book", on_delete=models.CASCADE)
    review_content = models.TextField(max_length=3000, null=False)
    review_rating = models.SmallIntegerField(default=0, null=False)
    review_like = models.SmallIntegerField(default=0)

