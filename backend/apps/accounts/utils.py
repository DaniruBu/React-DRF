from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

def send_activation_email(user):
    subject = 'Активация аккаунта'
    
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    
    message = f'Добро пожаловать на наш сайт! Активируйте ваш аккаунт, перейдя по ссылке: {settings.ACTIVATE_URL}/{uidb64}/{token}/'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)

def send_welcome_email(user):
    subject = 'Добро пожаловать!'
    message = f'Привет, {user.username}! Добро пожаловать на наш сайт! Ваш аккаунт успешно активирован.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)