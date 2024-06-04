from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Trade, Sell, Purchase

class TradeChartSerializer(ModelSerializer):
    class Meta:
        model = Trade
        fields = (
            "trade_date",
            "trade_price",
        )

class SellListSerializer(ModelSerializer):
    sell_count = SerializerMethodField()
    sell_price = SerializerMethodField()

    class Meta:
        model = Sell
        fields = (
            'sell_price',
            'sell_count'
        )

    def get_sell_count(self, sell):
        return sell['count']
    
    def get_sell_price(self, sell):
        return sell['sell_price']


class PurchaseListSerializer(ModelSerializer):
    purchase_count = SerializerMethodField()
    purchase_price = SerializerMethodField()

    class Meta:
        model = Purchase
        fields = (
            'purchase_price',
            'purchase_count'
        )

    def get_purchase_count(self, purchase):
        return purchase['count']
    
    def get_purchase_price(self, purchase):
        return purchase['purchase_price']
    
