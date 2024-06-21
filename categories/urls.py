from django.urls import path
from . import views

# URL과 뷰 클래스 매핑
urlpatterns = [
    path('<str:category_id>', views.Category.as_view()),
]