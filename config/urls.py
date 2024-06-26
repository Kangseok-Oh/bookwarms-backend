"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# 각 앱별 API URL 매핑
# 자세한 URL은 각 앱 내의 urls.py를 확인
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include("users.urls")),
    path('api/book/', include("books.urls")),
    path('api/category/', include("categories.urls")),
    path('api/bookshelf/', include("bookshelfs.urls")),
    path('api/cart/', include("carts.urls")),
    path('api/order/', include("orders.urls")),
    path('api/trade/', include("trades.urls")),
    path('api/review/', include("reviews.urls")),
]
