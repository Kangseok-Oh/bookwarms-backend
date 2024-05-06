import requests
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserInfoSerializer

class LogIn(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            raise ParseError()
        
        user = authenticate(request, user_email=email, password=password)
        
        if user:
            login(request, user)
            return Response({"ok": "welcome"})
        else:
            return Response({"error": "회원 이메일이 존재하지 않거나 비밀번호가 틀렸습니다."})
        
class KakaoLogIn(APIView):
    def post(self, request):
        try:
            code = request.data.get('code')
            access_token = requests.post("https://kauth.kakao.com/oauth/token",
                headers= {
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                data={
                    "grant_type": "authorization_code",
                    "client_id": "7dfce64ff304bf27077e66600b312895",
                    "redirect_uri": "http://127.0.0.1:3000/user/login/kakao",
                    "code": code,
                }
            )
            access_token = access_token.json().get('access_token')
            print(access_token)

            user_data = requests.get("https://kapi.kakao.com/v2/user/me",
                headers= {
                    "Authorization": f"Bearer {access_token}",
                    "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
                }
            )
            user_data = user_data.json()
            kakao_account = user_data.get('kakao_account')
            profile = kakao_account.get('profile')

            try:
                user = User.objects.get(user_email=kakao_account.get('email'))
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                user = User.objects.create(
                    user_email = kakao_account.get('email'),
                    user_name = profile.get('nickname'),
                )
                user.set_unusable_password()
                user.save()
                login(request, user)
                return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class LogOut(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        logout(request)
        return Response({"ok": "see you again"})
    
class UserInfo(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        serializer = UserInfoSerializer(user)
        return Response(serializer.data)

class SignUp(APIView):
    def post(self, request):
        user_profile = request.data
        email = user_profile.get('email')
        try:
            user = User.objects.get(user_email=email)
            return Response({"error": "이미 가입된 이메일입니다."}) 
        except User.DoesNotExist:
            user = User.objects.create(
                user_email = user_profile.get('email'),
                user_name = user_profile.get('name'),
                user_gender = user_profile.get('gender'),
                user_birth = user_profile.get('birth')
            )
            user.set_password(user_profile.get('password'))
            user.save()
            return Response({"ok": "welcome"})

