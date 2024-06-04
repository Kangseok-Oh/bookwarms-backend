from django.urls import path
from . import views

urlpatterns = [
    path('tradechart/<str:book_isbn>', views.TradeChart.as_view()),
    path('selllist/<str:book_isbn>', views.SellList.as_view()),
    path('purchaselist/<str:book_isbn>', views.PurchaseList.as_view()),
    path('immediate-sell-price/<str:book_isbn>', views.ImmediateSellPrice.as_view()),
    path('immediate-pur-price/<str:book_isbn>', views.ImmediatePurPrice.as_view()),
    path('sell', views.Sell.as_view()),
    path('purchase', views.Purchase.as_view()),
    path('immediate-sell', views.ImmediateSell.as_view()),
    path('immediate-purchase', views.ImmediatePurchase.as_view()),
]