from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from ai.utils.embeddings import embed_text
from ai.utils.message import assistant_talking, user_talking
from ai.utils.chats_handler import chats_handler, generate_chat_title

from .models import ChatSession, ChatMessage
from accounts.models import UserProfile
from .serializers import ChatSessionSerializer, ChatMessageSerializer

from ai.documents.tools.context_handler import get_next_questions

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

    print("[send_message] Request received", flush=True)

    user_content = request.data.get('user_content')
    session_id = request.data.get('session')
    print(f"[send_message] Input received: session_id={session_id}, has_user_content={bool(user_content)}", flush=True)

    # -------------------------
    # Validate input
    # -------------------------
    if not user_content or not user_content.strip():
        print("[send_message] Validation failed: user_content is missing or empty", flush=True)
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
            print(f"[send_message] Looking up session: {session_id}", flush=True)

            try:
                session = ChatSession.objects.get(
                    id=session_id,
                    user=request.user,
                    archived=False
                )

            except ChatSession.DoesNotExist:
                print(f"[send_message] Session not found: {session_id}", flush=True)
                return Response(
                    {
                        'error': 'Chat session not found.'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

        else:
            print("[send_message] Creating a new session", flush=True)
            session = ChatSession.objects.create(
                user=request.user)
        print(f"[send_message] Session ready: id={session.id}, use_case={session.use_case}", flush=True)
        if session.title == 'New Chat Session':

            try:
                print(f"[send_message] Generating title for session {session.id}", flush=True)
                session.title = generate_chat_title(user_content)
                session.save(update_fields=['title', 'updated_at'])
                print(f"[send_message] Title generated: {session.title}", flush=True)
            except Exception as e:
                print(f"Title generation error: {str(e)}", flush=True)

                # Fallback if LLM title generation fails
                session.title = "New Chat Session"
                session.save(update_fields=['title', 'updated_at'])
                print("[send_message] Using fallback title", flush=True)


        # Get chat history

        previous_messages = ChatMessage.objects.filter(
            session=session
        ).order_by('created_at')
        print(f"[send_message] Loading chat history for session {session.id}", flush=True)

        chat_history = []

        for message in previous_messages:

            if message.user_content:
                chat_history.append(user_talking(message.user_content))

            if message.assistant_content:
                chat_history.append(assistant_talking(message.assistant_content))
        print(f"[send_message] Chat history prepared: {len(chat_history)} entries", flush=True)

        # -------------------------
        # Generate embedding
        # -------------------------
        try:

            print("[send_message] Generating message embedding", flush=True)

            user_content_embedding = embed_text(
                user_content
            )
            print("[send_message] Message embedding generated", flush=True)

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
        print(f"\n===============================================\nNope : {session.id, session.use_case}", flush=True)
        print(f"[send_message] Context retrieval started for use_case={session.use_case}", flush=True)
        if session.use_case == "interview_assessment":
            # For interview_assessment, we can fetch relevant context from the database

            # user_profile  = UserProfile.objects.get_or_create(
            #         user=request.user
            #     )
            # In your view
            # user_profile = UserProfile.objects.get(user=request.user)
            # print(f"\n===============================================\nUser profile: {user_profile}", flush=True)

            # # Convert to dict
            # profile_data = {
            #     'primary_role': user_profile.primary_role,
            #     'target_role': user_profile.target_role,
            #     'experience_level': user_profile.experience_level,
            #     'skills': user_profile.skills,
            #     'education': user_profile.education,
            # }

            try:
                context_list = get_next_questions(
                    user = request.user,
                    user_content = user_content,
                    session_id = session.id,
                    top_k=1
                )
                context_parts = []
                if isinstance(context_list, dict) and context_list.get('status') == 'success':
                    question_data = context_list.get('question', {})
                    if question_data:
                        q_text = question_data.get('question', '')
                        q_answer = question_data.get('answer', '')
                        context_parts.append(f"Question: {q_text}\nAnswer: {q_answer}")
                context = "\n\n".join(context_parts)
                print(f"[send_message] Context retrieved: {len(context)} characters", flush=True)


            except Exception as e:

                print(
                    f"Context retrieval error: {str(e)}",
                    flush=True
                )

                return Response(
                    {
                        'error': 'Failed to retrieve relevant context.'
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        # -------------------------
        # Generate AI response
        # -------------------------
        try:

            print("[send_message] Generating AI response", flush=True)

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
        print(f"[send_message] Message saved: id={message.id}, session_id={session.id}", flush=True)

        # -------------------------
        # Serialize response
        # -------------------------
        message_serializer = ChatMessageSerializer(
            message
        )

        session_serializer = ChatSessionSerializer(
            session
        )
        print("[send_message] Response serialized successfully", flush=True)

        return Response(
            {
                'session': session_serializer.data,
                'message': message_serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    except Exception as e:

        print(
            f"[send_message] Unexpected error: {str(e)}",
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