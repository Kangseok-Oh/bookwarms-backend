from django.db import models

class Category(models.Model):
    category_id = models.CharField(max_length=2, primary_key=True)
    category_big_name = models.CharField(max_length=20, null=False)
    category_sml_name = models.CharField(max_length=20, null=False)
