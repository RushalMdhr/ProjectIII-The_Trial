from django.urls import path

from chats.views import sessions, get_messages, send_message,delete_session


urlpatterns = [
    path('session/', sessions, name='sessions'),
    path('message/', send_message, name='send_message'),
    path('session/<int:session_id>/messages', get_messages, name='get_messages'),
    path('session/<int:session_id>/delete', delete_session, name='delete_session')
]