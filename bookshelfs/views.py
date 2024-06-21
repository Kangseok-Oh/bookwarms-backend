from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from .models import BookshelfItem
from .serializers import BookshelfListSerializer

# 내 서재 책 리스트 API
class BookshelfList(APIView):
    # 로그인 시에만 호출 가능
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # 요청 보낸 유저의 이메일 추출
        user_email = request.user.user_email
        try:
            # 해당 유저의 내 서재 내의 책 데이터 조회
            bookshelf_list = BookshelfItem.objects.filter(bookshelf_user_email = user_email)
        except:
            # 없으면 오류
            raise NotFound
        # json 형식으로 변환 후 응답
        serializer = BookshelfListSerializer(bookshelf_list, many = True)
        return Response(serializer.data)