from django.urls import path
from common.views import health_check, say_hello, chat

urlpatterns = [
    path("health/", health_check),
    path("Rushal/", say_hello),
    path("chat/", chat),
]