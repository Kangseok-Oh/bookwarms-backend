from django.urls import path
from . import views

# URL과 뷰 클래스 매핑
urlpatterns = [
    path('bookdetail/<str:book_isbn>', views.BookDetail.as_view()),
    path('categorybooklist/<str:category_id>', views.CategoryBookList.as_view()),
    path('trade/<str:book_isbn>', views.TradeBook.as_view()),
    path('search/<str:key_word>', views.SearchList.as_view()),
]