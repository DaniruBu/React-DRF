from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import RegisterUserSerializer
from rest_framework.response import Response
from rest_framework import status
from .utils import send_welcome_email

class RegisterUserView(APIView):
    '''Регистрация пользователя'''
    permission_classes = [AllowAny]
    serializer_class = RegisterUserSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.is_active = True
        user.save()
        send_welcome_email(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

        