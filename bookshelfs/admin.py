from django.contrib import admin
from .models import Bookshelf, BookshelfItem

@admin.register(Bookshelf)
class BookshelfAdmin(admin.ModelAdmin):
    pass

@admin.register(BookshelfItem)
class BookshelfItemAdmin(admin.ModelAdmin):
    pass
