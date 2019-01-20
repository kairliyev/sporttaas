from django.urls import path
from users.views import UserRegistrationAPIView, UserLoginAPIView, UserTokenAPIView, UserLogoutAPIView

app_name = 'users'

urlpatterns = [
    path('users/', UserRegistrationAPIView.as_view(), name="list"),
    path('users/login/', UserLoginAPIView.as_view(), name="login"),
    path('users/logout/', UserLogoutAPIView.as_view(), name="logout"),
    path('tokens/<key>/', UserTokenAPIView.as_view(), name="token"),
]
