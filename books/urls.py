from django.urls import path
from . import views

urlpatterns = [
    path('categorybooklist/<str:category_id>', views.CategoryBookList.as_view()),
]