from django.db import models

# 책 카테고리 모델
class Category(models.Model):
    # 컬럼들
    category_id = models.CharField(max_length=2, primary_key=True)
    category_big_name = models.CharField(max_length=20, null=False)
    category_sml_name = models.CharField(max_length=20, null=False)
