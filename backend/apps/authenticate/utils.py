from django.conf import settings
from rest_framework.authentication import CSRFCheck
from rest_framework import exceptions
from functools import wraps

def set_jwt_cookies(response, token):
    response.set_cookie(
        key=settings.SIMPLE_JWT['REFRESH_COOKIE'],
        value=token,
        httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
    )
    return response

def delete_jwt_cookies(response):
    response.delete_cookie(
        key=settings.SIMPLE_JWT['REFRESH_COOKIE'],
        path='/',
        domain=None,
        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
    )
    return response

def enforce_csrf(func):
    """
    Декоратор для принудительной проверки CSRF
    """
    def dummy_get_response(_):
        return None
    @wraps(func)
    def _wrapped_view(request, *args, **kwargs):
        check = CSRFCheck(dummy_get_response)
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        if reason:
            raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)
        return func(request, *args, **kwargs)
    return _wrapped_view


