from django.urls import path
from . import views

urlpatterns = [
    path('<str:category_id>', views.Category.as_view()),
]