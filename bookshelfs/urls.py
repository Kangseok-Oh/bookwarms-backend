from django.urls import path
from .views import BookshelfList

# URL과 뷰 클래스 매핑
urlpatterns = [
    path('', BookshelfList.as_view())
]