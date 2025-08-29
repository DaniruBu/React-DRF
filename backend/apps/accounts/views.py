from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import RegisterUserSerializer
from rest_framework.response import Response
from rest_framework import status
from .utils import send_welcome_email, send_activation_email
from .models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

class RegisterUserView(APIView):
    '''Регистрация пользователя'''
    permission_classes = [AllowAny]
    serializer_class = RegisterUserSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.is_active = False  
        user.save()
        send_activation_email.delay(user.id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ActivateUserView(APIView):
    '''Активация пользователя по uidb64 и token'''
    permission_classes = [AllowAny]
    
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(User, pk=uid)
            
            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                send_welcome_email.delay(user.id)
                return Response({
                    'message': 'Аккаунт успешно активирован.'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'Неверный токен активации.'
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({
                'error': 'Неверная ссылка активации.'
            }, status=status.HTTP_400_BAD_REQUEST)

        