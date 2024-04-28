from django.contrib import admin
from .models import Wish, WishItem

@admin.register(Wish)
class WishAdmin(admin.ModelAdmin):
    pass

@admin.register(WishItem)
class WishItemAdmin(admin.ModelAdmin):
    pass
