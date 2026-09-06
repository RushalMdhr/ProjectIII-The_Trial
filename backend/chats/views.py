from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from ai.utils.embeddings import embed_text
from ai.utils.message import assistant_talking, user_talking
from ai.utils.chats_handler import chats_handler, generate_chat_title
from ai.utils.chats_handler import evaluate_interview_answer, profile_interview_context
from ai.documents.tools.context_handler import relevant_context
from accounts.models import UserProfile

from .models import ChatSession, ChatMessage, InterviewEvaluation
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
        interview_difficulty = request.data.get(
            'interview_difficulty',
            'medium'
        )
        if interview_difficulty not in {'easy', 'medium', 'hard'}:
            interview_difficulty = 'medium'
        session = ChatSession.objects.create(
            user=request.user,
            use_case=use_case,
            title=title,
            interview_difficulty=interview_difficulty,
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
                user=request.user)

        # Update chat title
        if session.title == 'New Chat Session':

            try:
                session.title = generate_chat_title(user_content)
                session.save(update_fields=['title', 'updated_at'])
            except Exception as e:
                print(f"Title generation error: {str(e)}", flush=True)

                # Fallback if LLM title generation fails
                session.title = "New Chat Session"
                session.save(update_fields=['title', 'updated_at'])


        # Get chat history

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

        context = ""
        print(f"===================================================================\n\t\t\t\tREFERENCE\n",flush=True)
        print(f"===================================================================\n",flush=True)
        interview_evaluation = None
        interview_question = None

        if session.use_case == 'interview_assessment':
            interview_question = next(
                (
                    message.assistant_content
                    for message in reversed(list(previous_messages))
                    if message.assistant_content
                ),
                None,
            )
            print(f"interview question : {interview_question}")

            profile, _ = UserProfile.objects.get_or_create(user=request.user)
            if interview_question:
                interview_evaluation = evaluate_interview_answer(
                    question=interview_question,
                    answer=user_content,
                )
                print(f"===================================================================\n\t\t\t\tInterview Qusetion\n {interview_question} \n",flush=True)
                print(f"===================================================================\n\t\t\t\tInterview Evaluation\n {interview_evaluation} \n",flush=True)
                print(f"===================================================================\n",flush=True)
                if interview_evaluation['score'] == 0:
                    context = 'Stop the interview immediately. The candidate response was non-responsive.'
                else:
                    session.interview_difficulty = (
                        'hard' if interview_evaluation['score'] == 10
                        else 'medium' if interview_evaluation['score'] >= 5
                        else 'easy'
                    )
                    session.save(update_fields=['interview_difficulty', 'updated_at'])
                    context_items = relevant_context(
                        f"{interview_question}\nCandidate answer: {user_content}",
                        difficulty=session.interview_difficulty,
                    )
                    context = '\n\n'.join(
                        f"Question: {item['question']}\n"
                        f"Ideal answer: {item['ideal_answer']}\n"
                        f"Difficulty: {item['difficulty']}"
                        for item in context_items
                    )
            else:
                profile_context = profile_interview_context(profile)
                context_items = relevant_context(
                    f"{profile.target_role} {profile.experience_level} {profile.skills}",
                    difficulty=session.interview_difficulty,
                )
                context = profile_context + '\n\n' + '\n\n'.join(
                    f"Suggested question: {item['question']}\n"
                    f"Difficulty: {item['difficulty']}"
                    for item in context_items
                )

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
            if interview_evaluation and interview_evaluation['score'] == 0:
                assistant_content = (
                    "The interview has ended because the response was not "
                    "relevant to the question."
                )

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
            assistant_content=assistant_content,
        )

        if interview_evaluation:
            InterviewEvaluation.objects.create(
                session=session,
                message=message,
                score=interview_evaluation['score'],
                difficulty=session.interview_difficulty,
                feedback=interview_evaluation['feedback'],
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