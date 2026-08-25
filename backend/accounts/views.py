import os

from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import get_user_model

from authlib.integrations.django_client import OAuth

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


User = get_user_model()



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
@api_view(['GET'])
def google_callback(request):
    token = oauth.google.authorize_access_token(request)

    user_info = token.get('userinfo')

    email = user_info.get('email')
    name = user_info.get('name', '')

    if not email:
        return Response({'error': 'Email not provided by Google'}, status=400)

    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            'first_name': name,
        }
    )

    if created and hasattr(user, 'set_unusable_password'):
        user.set_unusable_password()
        user.save(update_fields=['password'])

    return Response({
        'message': 'Google Authentication successful',
        'user_created': created,
        'user':{
            'id': user.id,
            'username': getattr(user, 'username', None),
            'email': user.email,
            'first_name': user.first_name,
        } ,
        'full information': user_info,
    })