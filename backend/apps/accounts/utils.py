from django.core.mail import send_mail
from django.conf import settings

def send_welcome_email(user):
    subject = 'Добро пожаловать!'
    message = f'Привет, {user.username}! Добро пожаловать на наш сайт! Ваш аккаунт успешно создан.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)