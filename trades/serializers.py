from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Trade, Sell, Purchase

# 거래 내역용 거래 데이터 json 형식 지정
class TradeChartSerializer(ModelSerializer):
    class Meta:
        model = Trade
        fields = (
            "trade_date",
            "trade_price",
        )

# 판매 입찰 내역용 판매 입찰 데이터 json 형식 지정
class SellListSerializer(ModelSerializer):
    sell_count = SerializerMethodField()
    sell_price = SerializerMethodField()

    class Meta:
        model = Sell
        fields = (
            'sell_price',
            'sell_count'
        )

    # 해당 가격에 입찰한 내역 개수
    def get_sell_count(self, sell):
        return sell['count']
    
    # 입찰가
    def get_sell_price(self, sell):
        return sell['sell_price']

# 구매 입찰 내역용 구매 입찰 데이터 json 형식 지정
class PurchaseListSerializer(ModelSerializer):
    purchase_count = SerializerMethodField()
    purchase_price = SerializerMethodField()

    class Meta:
        model = Purchase
        fields = (
            'purchase_price',
            'purchase_count'
        )

    # 해당 가격에 입찰한 내역 개수
    def get_purchase_count(self, purchase):
        return purchase['count']
    
    # 입찰가
    def get_purchase_price(self, purchase):
        return purchase['purchase_price']
    
