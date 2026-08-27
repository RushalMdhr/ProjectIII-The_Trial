from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView,)
from .views import google_login,google_callback, login_account, register_account, test_account, me

urlpatterns = [
    path('test/', test_account),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', me, name='me'),
    path('google/login/', google_login, name='google_login'),
    path('google/callback/', google_callback, name='google_callback'),
    path('register/',register_account, name='register_account'),
    path('login/',login_account, name='login_account'),
]