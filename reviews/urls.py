from django.urls import path
from . import views

urlpatterns = [
    path('reviewlist/<str:book_isbn>', views.ReviewList.as_view()),
    path('submit-review', views.submitReview.as_view())
]