import os
import json
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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
        'email': request.user.email,
        'first_name': request.user.first_name,
        'profile_picture': request.user.profile_picture,
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

    google_id = user_info.get('sub')
    email = user_info.get('email')
    name = user_info.get('name', '')
    picture = user_info.get('picture')

    user, created = User.objects.get_or_create(
        google_id=google_id,
        defaults={
            'email': email,
            'first_name': name,
            'profile_picture': picture,
        }
    )

    if created:
        user.set_unusable_password()
        user.save(update_fields=['password'])

    refresh = RefreshToken.for_user(user)

    return Response({
        'message': 'Google authentication successful',
        'user': {
            'id': user.id,
            'google_id': google_id,
            'email': user.email,
            'first_name': user.first_name,
            'profile_picture': user.profile_picture,
        },
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    })


@csrf_exempt
def test_connect(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message = data.get("message", "")
            print("Message received from frontend:", message)

            return JsonResponse({
                "success": True,
                "message": f"Backend received: {message}"
            })
        except Exception:
            return JsonResponse({
                "success": False,
                "message": "Invalid request payload."
            }, status=400)

    return JsonResponse({
        "success": False,
        "message": "Only POST requests are allowed."
    }, status=405)

@api_view(['POST'])
def register_account(request):
    name = request.data.get('name') or request.data.get('first_name') or ''
    email = request.data.get('email')
    password = request.data.get('password')

    # Check required fields
    if not email or not password:
        return Response({
            'success': False,
            'message': 'Email and password are required.'
        }, status=400)

    # Check email
    if User.objects.filter(email=email).exists():
        return Response({
            'success': False,
            'message': 'Email already exists.'
        }, status=400)

    username_base = email.split('@', 1)[0][:150] or 'user'
    username = username_base
    suffix = 1
    while User.objects.filter(username=username).exists():
        suffix_text = str(suffix)
        username = f'{username_base[:150 - len(suffix_text)]}{suffix_text}'
        suffix += 1

    # Create user
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=name
    )

    return Response({
        'success': True,
        'message': 'Account created successfully.',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name
        }
    }, status=201)

@api_view(['POST'])
def login_account(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({
            'message': 'Invalid email or password'
        }, status=400)

    if not user.check_password(password):
        return Response({
            'message': 'Invalid email or password'
        }, status=400)

    refresh = RefreshToken.for_user(user)

    return Response({
        'success': True,
        'message': 'Login successful',
        'user': {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'profile_picture': user.profile_picture,
        },
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    })