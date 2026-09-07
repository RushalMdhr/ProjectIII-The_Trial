from accounts.models import UserProfile
from .connection import get_db_cursor
from django.db import connection
from ai.utils.embeddings import embed_text_local, embed_text


def get_next_questions(user, user_content, session_id, top_k=5):
    print("[context_handler] get_next_questions started", flush=True)
    print(f"[context_handler] user={user}, session_id={session_id}, top_k={top_k}", flush=True)
    print(f"[context_handler] user_content={user_content!r}", flush=True)

    # 1. Get user's profile
    print("[context_handler] Loading user profile", flush=True)
    try:
        profile = UserProfile.objects.get(user=user)
        print("[context_handler] Profile found", flush=True)
    except UserProfile.DoesNotExist:
        print("[context_handler] No user profile found", flush=True)
        return {
            "status": "error",
            "message": "Please provide your target role first."
        }

    # 2. Stop if no target role
    print(f"[context_handler] Profile target_role={profile.target_role!r}", flush=True)
    if not profile.target_role:
        print("[context_handler] Target role is missing", flush=True)
        return {
            "status": "missing_role",
            "message": "Please provide your target role first."
        }
    
    role = profile.target_role
    print(f"[context_handler] Using target role: {role!r}", flush=True)

    # 3. Embed the user's current message
    print("[context_handler] Generating query embedding", flush=True)
    query_embedding = embed_text(user_content)
    print(
            f"[context_handler] Query embedding generated: {query_embedding is not None}",
            flush=True
        )

    # 4. Retrieve relevant questions from pgvector
    print("[context_handler] Opening database connection for question retrieval", flush=True)
    with connection.cursor() as cur:
        print(
            f"[context_handler] Executing question query for role={role!r}, "
            f"session_id={session_id}, top_k={top_k}",
            flush=True
        )

        cur.execute("""
            SELECT
                iq.id,
                iq.question,
                iq.answer,
                iq.role,
                iq.experience,
                iq.difficulty,
                iq.keywords,
                iq.embedding <=> %s::vector AS distance

            FROM common_interviewquestions iq

            WHERE LOWER(iq.role) = LOWER(%s)

            -- Don't retrieve questions already asked
            AND iq.id NOT IN (
                SELECT question_id
                FROM common_askedquestions
                WHERE session_id = %s
            )

            ORDER BY iq.embedding <=> %s::vector

            LIMIT %s;
        """, (
            query_embedding,
            role,
            session_id,
            query_embedding,
            top_k
        ))

        questions = cur.fetchall()
        print(f"[context_handler] Retrieved {len(questions)} question(s)", flush=True)

    # 5. No questions available
    if not questions:
        print("[context_handler] No unused questions available", flush=True)
        return {
            "status": "finished",
            "message": "No more unused questions are available for this role."
        }

    # 6. Select the best retrieved question
    selected_question = questions[0]
    print(f"[context_handler] Selected question row: {selected_question}", flush=True)

    question_id = selected_question[0]
    print(
        f"[context_handler] Selected question ID: {question_id} for session ID: {session_id}",
        flush=True
    )
    # 7. Record ONLY the question actually asked
    print("[context_handler] Opening database connection to record asked question", flush=True)
    with connection.cursor() as cur:
        print(
            f"[context_handler] Recording question_id={question_id} for session_id={session_id}",
            flush=True
        )

        cur.execute("""
            INSERT INTO common_askedquestions
                (session_id, question_id, asked_at)

            VALUES (%s, %s, NOW());
        """, (
            session_id,
            question_id
        ))
        print("[context_handler] Asked question recorded", flush=True)

    # 8. Return the selected question
    response = {
        "status": "success",
        "role": role,
        "question": {
            "id": selected_question[0],
            "question": selected_question[1],
            "answer": selected_question[2],
            "role": selected_question[3],
            "experience": selected_question[4],
            "difficulty": selected_question[5],
            "keywords": selected_question[6],
            "distance": selected_question[7],
        }
    }
    print(f"[context_handler] Returning response: {response}", flush=True)
    print("[context_handler] get_next_questions finished", flush=True)
    return response