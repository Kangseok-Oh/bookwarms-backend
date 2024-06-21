import requests
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserInfoSerializer

# 로그인 API
class LogIn(APIView):
    def post(self, request):
        # 파라미터에서 이메일, 패스워드 추출
        email = request.data.get('email')
        password = request.data.get('password')

        # 이메일이나 패스워드 데이터 없으면 오류
        if not email or not password:
            raise ParseError()
        
        # 유저 정보 조회
        user = authenticate(request, user_email=email, password=password)
        
        # 해당 유저 확인하면 로그인 후 응답
        if user:
            login(request, user)
            return Response({"ok": "welcome"})
        # 해당 유저 없으면 오류 응답
        else:
            return Response({"error": "회원 이메일이 존재하지 않거나 비밀번호가 틀렸습니다."})

# 카카오 로그인 API  
class KakaoLogIn(APIView):
    def post(self, request):
        try:
            # 파라미터에서 코드 추출
            code = request.data.get('code')

            # 카카오에 코드를 담은 post 요청 보내 엑세스 토큰 응답 받기
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

            # 응답 데이터에서 엑세스 토큰 추출
            access_token = access_token.json().get('access_token')
            print(access_token)

            # 카카오에 엑세스 토큰 담아 회원 정보 get 요청
            user_data = requests.get("https://kapi.kakao.com/v2/user/me",
                headers= {
                    "Authorization": f"Bearer {access_token}",
                    "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
                }
            )

            # 응답에서 회원 정보 추출
            user_data = user_data.json()
            kakao_account = user_data.get('kakao_account')
            profile = kakao_account.get('profile')

            try:
                # 카카오에 등록된 이메일과 같은 이메일의 유저가 있는지 조회
                user = User.objects.get(user_email=kakao_account.get('email'))
                # 있으면 그냥 로그인 후 ok 응답
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                # 카카오에 등록된 이메일과 같은 이메일의 유저가 없으면 새로 생성
                user = User.objects.create(
                    user_email = kakao_account.get('email'),
                    user_name = profile.get('nickname'),
                )

                # 소셜 로그인은 패스워드 사용하지 않으므로 무작위 패스워드 생성
                user.set_unusable_password()
                user.save()

                # 로그인 후 ok 응답
                login(request, user)
                return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
# 로그아웃 API
class LogOut(APIView):
    # 로그인 시에만 API 호출 가능
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 로그아웃 후 ok 응답
        logout(request)
        return Response({"ok": "see you again"})

# 화면 헤더에 띄워줄 회원 정보 API 
class UserInfo(APIView):
    # 로그인 시에만 API 호출 가능
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # 요청 보낸 유저 조회
        user = request.user
        # 해당 유저 데이터 json 변환 후 응답
        serializer = UserInfoSerializer(user)
        return Response(serializer.data)

# 회원 가입 API
class SignUp(APIView):
    def post(self, request):
        # 회원 가입 데이터 추출
        user_profile = request.data
        email = user_profile.get('email')
        try:
            # 해당 이메일로 가입한 유저 있는지 조회
            user = User.objects.get(user_email=email)
            # 있으면 오류 응답
            return Response({"error": "이미 가입된 이메일입니다."}) 
        except User.DoesNotExist:
            # 없으면 새로운 회원 로우 생성
            user = User.objects.create(
                user_email = user_profile.get('email'),
                user_name = user_profile.get('name'),
                user_gender = user_profile.get('gender'),
                user_birth = user_profile.get('birth')
            )
            user.set_password(user_profile.get('password'))
            user.save()
            # ok 응답
            return Response({"ok": "welcome"})

