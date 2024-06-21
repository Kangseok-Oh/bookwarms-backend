from django.urls import path
from . import views

# URL과 뷰 클래스 매핑
urlpatterns = [
    path('reviewlist/<str:book_isbn>', views.ReviewList.as_view()),
    path('submit-review', views.submitReview.as_view())
]