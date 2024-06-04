from django.urls import path
from . import views

urlpatterns = [
    path('bookdetail/<str:book_isbn>', views.BookDetail.as_view()),
    path('categorybooklist/<str:category_id>', views.CategoryBookList.as_view()),
    path('trade/<str:book_isbn>', views.TradeBook.as_view())
]