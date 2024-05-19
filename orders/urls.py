from django.urls import path
from .views import OrderList, Order

urlpatterns = [
    path('', OrderList.as_view()),
    path('payment', Order.as_view()),
]