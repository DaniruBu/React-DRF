from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils.decorators import method_decorator
from django.middleware import csrf
from .utils import set_jwt_cookies, delete_jwt_cookies, delete_csrf_cookie, enforce_csrf
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status


def get_tokens(response):
    access_token = response.data.get('access')
    refresh_token = response.data.get('refresh')
    if access_token and refresh_token:
        response = set_jwt_cookies(response, refresh_token)
        del response.data['refresh']
    return response

class CookieTokenObtainPairView(TokenObtainPairView):
    """
    Представление для получения JWT-токенов (access и refresh) и сохранения refresh в куки
    """
    @method_decorator(enforce_csrf)
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            response = get_tokens(response)
            csrf.get_token(request)
        return response

class CookieTokenRefreshView(TokenRefreshView):
    """
    Представление для обновления JWT-токенов (access и refresh) с использованием кук
    """
    @method_decorator(enforce_csrf)
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT['REFRESH_COOKIE'])
        
        data = {'refresh': refresh_token}
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        response = Response(serializer.validated_data, status=status.HTTP_200_OK)
        response = get_tokens(response)
        
        csrf.get_token(request)
        
        return response


class CookieTokenLogoutView(TokenRefreshView):
    """
    Представление для выхода из системы (logout) с очисткой cookies
    """
    @method_decorator(enforce_csrf)
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT['REFRESH_COOKIE'])
        
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except (TokenError, InvalidToken):
                pass
        
        response = Response(status=status.HTTP_200_OK)
        response = delete_jwt_cookies(response)
        response = delete_csrf_cookie(response)
        
        return response


