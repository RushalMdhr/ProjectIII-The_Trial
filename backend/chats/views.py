from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from ai.utils.embeddings import embed_text
from ai.utils.message import assistant_talking, user_talking
from ai.utils.chats_handler import (
    chats_handler,
    evaluate_interview_answer,
    generate_chat_title,
)

from .models import ChatSession, ChatMessage, InterviewFeedback
from accounts.models import UserProfile
from .serializers import ChatSessionSerializer, ChatMessageSerializer

from ai.documents.tools.context_handler import get_next_questions


INTERVIEW_LIMITS = {
    "easy": 5,
    "medium": 8,
    "hard": 10,
}

DIFFICULTY_LEVELS = {"easy": 0, "medium": 1, "hard": 2}


def _update_interview_level(session, rating):
    ceiling = DIFFICULTY_LEVELS[session.interview_difficulty]
    current = DIFFICULTY_LEVELS[session.current_difficulty]
    if rating >= 8:
        current += 1
    elif rating <= 4:
        current -= 1
    current = max(0, min(current, ceiling))
    session.current_difficulty = next(
        name for name, level in DIFFICULTY_LEVELS.items() if level == current
    )

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
            'medium',
        )
        if interview_difficulty not in INTERVIEW_LIMITS:
            return Response(
                {'error': 'Invalid interview difficulty.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        session = ChatSession.objects.create(
            user=request.user,
            use_case=use_case,
            title=title,
            interview_difficulty=interview_difficulty,
            current_difficulty='easy',
            max_questions=INTERVIEW_LIMITS[interview_difficulty],
        )
        print(
            f"[INTERVIEW] CREATED session_id={session.id} "
            f"selected_difficulty={session.interview_difficulty!r} "
            f"current_difficulty={session.current_difficulty!r} "
            f"max_questions={session.max_questions}",
            flush=True,
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
        print(
            f"[INTERVIEW] SESSION id={session.id} use_case={session.use_case!r} "
            f"ceiling={session.interview_difficulty!r} "
            f"current={session.current_difficulty!r} "
            f"count={session.question_count}/{session.max_questions} "
            f"archived={session.archived} halted={session.halted}",
            flush=True,
        )
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
        previous_question = next(
            (
                message for message in reversed(previous_messages)
                if message.question_text
            ),
            None,
        )
        print(f"[send_message] Loading chat history for session {session.id}", flush=True)

        chat_history = []
        halt_response = None

        for message in previous_messages:

            if message.user_content:
                chat_history.append(user_talking(message.user_content))

            if message.assistant_content:
                chat_history.append(assistant_talking(message.assistant_content))
        print(f"[send_message] Chat history prepared: {len(chat_history)} entries", flush=True)

        evaluation_rating = None
        evaluation_feedback = None
        if session.use_case == "interview_assessment" and previous_question:
            evaluation_rating, evaluation_feedback = evaluate_interview_answer(
                previous_question.question_text,
                previous_question.question_answer or "",
                user_content,
            )
            previous_question.evaluation_rating = evaluation_rating
            previous_question.evaluation_feedback = evaluation_feedback
            previous_question.save(update_fields=[
                "evaluation_rating",
                "evaluation_feedback",
            ])

            InterviewFeedback.objects.update_or_create(
                session=session,
                message=previous_question,
                defaults={
                    "rating": evaluation_rating,
                    "feedback": evaluation_feedback,
                },
            )

            _update_interview_level(session, evaluation_rating)
            print(
                f"[INTERVIEW] EVALUATION question={previous_question.question_text!r} "
                f"rating={evaluation_rating}/10 feedback={evaluation_feedback!r}",
                flush=True,
            )
            session.save(update_fields=["current_difficulty", "updated_at"])
            print(
                f"[INTERVIEW] ADAPT next_difficulty={session.current_difficulty!r} "
                f"ceiling={session.interview_difficulty!r}",
                flush=True,
            )
            if evaluation_rating <= 1:
                session.halted = True
                session.archived = True
                halt_response = (
                    "Interview paused because the answer was not relevant. "
                    "Please restart when you are ready to continue."
                )
                session.save(update_fields=[
                    "current_difficulty",
                    "halted",
                    "archived",
                    "updated_at",
                ])
            elif session.question_count >= session.max_questions:
                session.archived = True
                session.save(update_fields=["current_difficulty", "archived", "updated_at"])
                halt_response = "Interview complete. Your selected question limit has been reached."

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
        context_list = None
        print(f"\n===============================================\nNope : {session.id, session.use_case}", flush=True)
        print(f"[send_message] Context retrieval started for use_case={session.use_case}", flush=True)
        if session.use_case == "interview_assessment" and not session.halted and not halt_response:
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
                print(
                    f"[INTERVIEW] RAG RESULT status={context_list.get('status')!r} "
                    f"generated={context_list.get('generated', False)}",
                    flush=True,
                )
                if context_list.get('status') == 'missing_role':
                    session.halted = True
                    session.archived = True
                    session.save(update_fields=['halted', 'archived', 'updated_at'])
                    halt_response = (
                        "Interview paused. Please add your target role to your profile "
                        "before answering interview questions."
                    )
                elif context_list.get('status') == 'finished':
                    session.archived = True
                    session.save(update_fields=['archived', 'updated_at'])
                    halt_response = "Interview complete. No more questions are available for this role."
                context_parts = []
                if isinstance(context_list, dict) and context_list.get('status') == 'success':
                    question_data = context_list.get('question', {})
                    if question_data:
                        q_text = question_data.get('question', '')
                        q_answer = question_data.get('answer', '')
                        context_parts.append(f"Question: {q_text}\nAnswer: {q_answer}")
                        print(
                            f"[INTERVIEW] QUESTION id={question_data.get('id')} "
                            f"source_id={question_data.get('source_id')} "
                            f"role={question_data.get('role')!r} "
                            f"difficulty={question_data.get('difficulty')!r} "
                            f"distance={question_data.get('distance')} "
                            f"text={q_text!r}",
                            flush=True,
                        )
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

            if halt_response:
                result = {
                    "user_content": user_content,
                    "assistant_content": halt_response,
                }
            else:
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
            question_text=(
                context_list.get('question', {}).get('question')
                if context_list and context_list.get('status') == 'success'
                else None
            ),
            question_answer=(
                context_list.get('question', {}).get('answer')
                if context_list and context_list.get('status') == 'success'
                else None
            ),
            question_difficulty=(
                context_list.get('question', {}).get('difficulty')
                if context_list and context_list.get('status') == 'success'
                else None
            ),
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