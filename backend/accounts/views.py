import os

from django.conf import settings
from django.shortcuts import redirect

from authlib.integrations.django_client import OAuth

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response



# Google OAuth configuration
oauth = OAuth()

oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile',
    },
)



# Test endpoint

@api_view(['GET'])
def test_account(request):
    return Response({
        'message': 'Accounts API is working'
    })



# Current authenticated user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    return Response({
        'id': request.user.id,
        'username': request.user.username,
        'email': request.user.email,
    })



# Google Login

def google_login(request):
    redirect_uri = settings.GOOGLE_REDIRECT_URI

    return oauth.google.authorize_redirect(
        request,
        redirect_uri
    )



# Google Callback

def google_callback(request):
    token = oauth.google.authorize_access_token(request)

    user_info = token.get('userinfo')

    return Response({
        'message': 'Google authentication successful',
        'user': user_info,
    })