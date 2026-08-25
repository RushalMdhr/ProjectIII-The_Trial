from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView,)
from .views import google_login, test_account, me

urlpatterns = [
    path('test/', test_account),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', me, name='me'),
    path('google/login/', google_login, name='google_login'),
]