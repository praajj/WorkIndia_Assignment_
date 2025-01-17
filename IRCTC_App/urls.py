from django.urls import path
from .views import UserDetailAPI,RegisterUserAPIView
from .views import LoginView
urlpatterns = [
  path('register',RegisterUserAPIView.as_view()),
  path('login/', LoginView.as_view(), name='login'),
]