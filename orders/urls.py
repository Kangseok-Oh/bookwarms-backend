from django.urls import path
from .views import OrderList, Order

# URL과 뷰 클래스 매핑
urlpatterns = [
    path('', OrderList.as_view()),
    path('payment', Order.as_view()),
]