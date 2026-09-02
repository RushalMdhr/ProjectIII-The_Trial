from django.urls import path
from common.views import *

urlpatterns = [
    path("health/", health_check),
    path("Rushal/", say_hello),
    path("chat/", chat),
    path("embed/", SimpleSave),
    path("talktoai/", TalkToAi),
]