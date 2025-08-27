from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.CookieTokenObtainPairView.as_view(), name='login'),
    path('refresh/', views.CookieTokenRefreshView.as_view(), name='refresh'),
    path('logout/', views.CookieTokenLogoutView.as_view(), name='logout'),
]