from django.urls import path
from .views import CartList, AddCart, DeleteCart

urlpatterns = [
    path("", CartList.as_view()),
    path("add", AddCart.as_view()),
    path("delete", DeleteCart.as_view()),
]