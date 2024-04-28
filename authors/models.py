from django.db import models

class Author(models.Model):
    author_id = models.CharField(max_length=5, primary_key=True)
    author_name = models.CharField(max_length=100, null=False)
    author_nationality = models.CharField(max_length=100)
    author_scholarship = models.TextField(max_length=500)
    author_career = models.TextField(max_length=500)
    author_award = models.TextField(max_length=500)
