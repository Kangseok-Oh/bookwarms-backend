from django.contrib import admin
from .models import Trade, Sell, Purchase

@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    pass


@admin.register(Sell)
class SellAdmin(admin.ModelAdmin):
    pass

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    pass
