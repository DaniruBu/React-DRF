from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('activate/<str:uidb64>/<str:token>/', views.ActivateUserView.as_view(), name='activate'),
]
