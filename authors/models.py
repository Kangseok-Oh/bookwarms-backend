from django.db import models

# 작가 모델
class Author(models.Model):
    # 컬럼들
    author_id = models.CharField(max_length=5, primary_key=True)
    author_name = models.CharField(max_length=100, null=False)
    author_nationality = models.CharField(max_length=100)
    author_scholarship = models.TextField(max_length=500, null=True, blank=True)
    author_career = models.TextField(max_length=500, null=True, blank=True)
    author_award = models.TextField(max_length=500, null=True, blank=True)
    author_intro = models.TextField(max_length=500, null=True)
