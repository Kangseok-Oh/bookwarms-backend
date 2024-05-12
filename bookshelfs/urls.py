from django.urls import path
from .views import BookshelfList

urlpatterns = [
    path('', BookshelfList.as_view())
]