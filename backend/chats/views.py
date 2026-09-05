from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from ai.utils.embeddings import embed_text
from ai.utils.message import assistant_talking, user_talking
from ai.utils.chats_handler import chats_handler

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

        use_case = request.data.get(
            'use_case',
            'general_chat'
        )

        valid_use_cases = [
            choice[0]
            for choice in ChatSession.USE_CASE_CHOICES
        ]

        if use_case not in valid_use_cases:
            return Response(
                {
                    'error': 'Invalid use_case.',
                    'valid_use_cases': valid_use_cases
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        title = request.data.get(
            'title',
            'New Chat Session')
        session = ChatSession.objects.create(
            user=request.user,
            use_case=use_case,
            title=title
        )

        serializer = ChatSessionSerializer(session)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):

    print("Request reached here", flush=True)

    user_content = request.data.get('user_content')
    session_id = request.data.get('session')

    # -------------------------
    # Validate input
    # -------------------------
    if not user_content or not user_content.strip():
        return Response(
            {
                'error': 'user_content is required.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    try:

        # -------------------------
        # Get existing session OR create new session
        # -------------------------
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

        # -------------------------
        # Get chat history
        # -------------------------
        previous_messages = ChatMessage.objects.filter(
            session=session
        ).order_by('created_at')

        chat_history = []

        for message in previous_messages:

            if message.user_content:
                chat_history.append(user_talking(message.user_content))

            if message.assistant_content:
                chat_history.append(assistant_talking(message.assistant_content))

        # -------------------------
        # Generate embedding
        # -------------------------
        try:

            user_content_embedding = embed_text(
                user_content
            )

        except Exception as e:

            print(
                f"Embedding error: {str(e)}",
                flush=True
            )

            return Response(
                {
                    'error': 'Failed to generate message embedding.'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # -------------------------
        # Get context
        # -------------------------
        # For now context is empty.
        # Later this will come from your RAG pipeline.

        context = ""

        # -------------------------
        # Generate AI response
        # -------------------------
        try:

            result = chats_handler(
                user_content=user_content,
                chat_history=chat_history,
                context=context,
                use_case=session.use_case,
            )

            assistant_content = result["assistant_content"]

            print(
                "AI response generated successfully",
                flush=True
            )

            print(
                "Assistant response length:",
                len(assistant_content),
                flush=True
            )

        except Exception as e:

            print(
                f"Error generating AI response: {str(e)}",
                flush=True
            )

            return Response(
                {
                    'error': 'Failed to generate AI response.',
                    'details': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # -------------------------
        # Save message
        # -------------------------
        message = ChatMessage.objects.create(
            session=session,
            user=request.user,
            user_content=result["user_content"],
            user_content_embedding=user_content_embedding,
            assistant_content=result["assistant_content"],
        )

        # -------------------------
        # Serialize response
        # -------------------------
        message_serializer = ChatMessageSerializer(
            message
        )

        session_serializer = ChatSessionSerializer(
            session
        )

        return Response(
            {
                'session': session_serializer.data,
                'message': message_serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    except Exception as e:

        print(
            f"send_message error: {str(e)}",
            flush=True
        )

        return Response(
            {
                'error': 'Something went wrong while processing your message.',
                'details': str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_messages(request, session_id):

    # Get the session belonging to the authenticated user
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

    # Get messages for this session
    messages = ChatMessage.objects.filter(
        session=session,
        user=request.user
    ).order_by('-created_at')

    # Optional limit
    limit = request.query_params.get('limit')

    if limit is not None:
        try:
            limit = int(limit)

            if limit <= 0:
                return Response(
                    {
                        'error': 'limit must be greater than 0.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Fetch latest N messages
            messages = messages[:limit]

        except ValueError:
            return Response(
                {
                    'error': 'limit must be an integer.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    # Return messages in chronological order
    messages = messages.order_by('created_at')

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