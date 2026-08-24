from django.urls import path
from .views import test_account

urlpatterns = [
    path('test/', test_account),
]