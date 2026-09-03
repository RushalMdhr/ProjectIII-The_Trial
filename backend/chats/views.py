from django.http import HttpResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import ChatSession, ChatMessage
from .serializers import ChatSessionSerializer, ChatMessageSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def sessions(request):

    if request.method == 'GET':
        sessions = ChatSession.objects.filter(
            user=request.user,
            archived=False
        ).order_by('-updated_at')

        serializer = ChatSessionSerializer(
            sessions,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    if request.method == 'POST':
        session = ChatSession.objects.create(
            user=request.user
        )

        serializer = ChatSessionSerializer(session)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):

    user_content = request.data.get('user_content')
    session_id = request.data.get('session_id')

    if not user_content:
        return Response(
            {
                'error': 'user_content is required.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # 1. Get existing session OR create a new session
    if session_id:

        try:
            session = ChatSession.objects.get(
                id=session_id,
                user=request.user,
                archived=False
            )

        except ChatSession.DoesNotExist:
            return Response(
                {
                    'error': 'Chat session not found.'
                },
                status=status.HTTP_404_NOT_FOUND
            )

    else:

        session = ChatSession.objects.create(
            user=request.user
        )

    # 2. Temporary AI response

    assistant_content = f"AI response to: {user_content}"

    # 3. Create message

    message = ChatMessage.objects.create(
        session=session,
        user=request.user,
        user_content=user_content,
        assistant_content=assistant_content
    )

    # 4. Return response

    message_serializer = ChatMessageSerializer(message)
    session_serializer = ChatSessionSerializer(session)

    return Response(
        {
            'session': session_serializer.data,
            'message': message_serializer.data
        },
        status=status.HTTP_201_CREATED
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_messages(request, session_id):

    try:
        session = ChatSession.objects.get(
            id=session_id,
            user=request.user,
            archived=False
        )
    except ChatSession.DoesNotExist:
        return Response(
            {
                'error': 'Chat session not found.'
            },
            status=status.HTTP_404_NOT_FOUND
        )

    messages = ChatMessage.objects.filter(
        session=session,
        user=request.user
    ).order_by('created_at')

    serializer = ChatMessageSerializer(
        messages,
        many=True
    )

    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_session(request, session_id):

    try:
        session = ChatSession.objects.get(
            id=session_id,
            user=request.user,
            archived=False
        )
    except ChatSession.DoesNotExist:
        return Response(
            {'error': 'Chat session not found.'},
            status=status.HTTP_404_NOT_FOUND
        )

    session.archived = True
    session.save()

    return Response(
        {
            'message': 'Chat session archived successfully.'
        },
        status=status.HTTP_200_OK
    )