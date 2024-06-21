from django.urls import path
from .views import LogIn, LogOut, UserInfo, SignUp, KakaoLogIn

# 각 URL과 뷰 클래스 매핑
urlpatterns = [
    path("login", LogIn.as_view()),
    path("login/kakao", KakaoLogIn.as_view()),
    path("logout", LogOut.as_view()),
    path("me", UserInfo.as_view()),
    path("signup", SignUp.as_view()),
]