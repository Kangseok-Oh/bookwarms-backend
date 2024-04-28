from django.db import models

class Book(models.Model):
    book_isbn = models.CharField(max_length=13, primary_key=True)
    book_name = models.CharField(max_length=100, null=False)
    book_price = models.PositiveIntegerField(null=False)
    book_intro = models.TextField(max_length=3000, null=True, blank=True)
    book_contents = models.TextField(max_length=500, null=True, blank=True)
    book_total_words = models.CharField(max_length=5, null=True, blank=True)
    book_publisher = models.CharField(max_length=50)
    book_interpreter = models.CharField(max_length=50)
    book_cover_path = models.URLField(null=True, blank=True)
    book_ebook_path = models.URLField(null=False)
    book_category_id = models.ForeignKey("categories.Category", null= True, on_delete=models.SET_NULL)
    book_author_id = models.ForeignKey("authors.Author", null = True, on_delete=models.SET_NULL)

    def book_rating(self):
        review_count = self.review_set.count()
        if review_count == 0:
            return 0
        else:
            total_rating = 0
            for review in self.review_set.all().values("review_rating"):
                total_rating += review["review_rating"]
            return round(total_rating/ review_count, 2)
        
    def book_review_count(self):
        return self.review_set.count()

