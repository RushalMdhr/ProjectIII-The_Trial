from accounts.models import UserProfile
from chats.models import ChatSession
from .connection import get_db_cursor
from django.db import connection
from ai.llm import ai
from ai.utils.message import system_talking
from ai.utils.embeddings import embed_text_local, embed_text


DIFFICULTY_LEVELS = {"easy": 0, "medium": 1, "hard": 2}


def _default_question(role, difficulty):
    print(
        f"[INTERVIEW-RAG] FALLBACK generation started role={role!r} "
        f"difficulty={difficulty!r}",
        flush=True,
    )
    difficulty = "hard"
    prompt = (
        "Generate one concise interview question only. Do not add an answer, "
        f"markdown, numbering, or explanation. The target role is {role} and "
        f"the difficulty is {difficulty}."
    )
    try:
        question = str(ai([system_talking(prompt)])).strip()
        question = question.splitlines()[0].strip(" -*0123456789.:")
        if question:
            print(
                f"[INTERVIEW-RAG] FALLBACK generated question={question!r}",
                flush=True,
            )
            return question
    except Exception as error:
        print(f"[context_handler] Default question generation failed: {error}", flush=True)
    fallback = f"Describe a recent {difficulty}-level problem you solved as a {role}."
    print(f"[INTERVIEW-RAG] FALLBACK static question={fallback!r}", flush=True)
    return fallback


def get_next_questions(user, user_content, session_id, top_k=5):
    print("[context_handler] get_next_questions started", flush=True)
    print(f"[context_handler] user={user}, session_id={session_id}, top_k={top_k}", flush=True)
    print(f"[context_handler] user_content={user_content!r}", flush=True)

    session = ChatSession.objects.get(id=session_id, user=user, archived=False)
    print(
        "[INTERVIEW-RAG] SESSION "
        f"id={session.id} selected_ceiling={session.interview_difficulty!r} "
        f"current_difficulty={session.current_difficulty!r} "
        f"question_count={session.question_count}/{session.max_questions}",
        flush=True,
    )

    # 1. Get user's profile
    print("[context_handler] Loading user profile", flush=True)
    try:
        profile = UserProfile.objects.get(user=user)
        print("[context_handler] Profile found", flush=True)
    except UserProfile.DoesNotExist:
        print("[context_handler] No user profile found", flush=True)
        return {
            "status": "missing_role",
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
    print(f"[INTERVIEW-RAG] PROFILE role={role!r}", flush=True)
    session.interview_role = role
    session.save(update_fields=["interview_role", "updated_at"])
    print(f"[context_handler] Using target role: {role!r}", flush=True)

    target_level = DIFFICULTY_LEVELS.get(session.interview_difficulty, 1)
    current_level = min(
        DIFFICULTY_LEVELS.get(session.current_difficulty, 0),
        target_level,
    )
    current_difficulty = next(
        difficulty for difficulty, level in DIFFICULTY_LEVELS.items()
        if level == current_level
    )
    print(
        f"[INTERVIEW-RAG] FILTER role={role!r} difficulty={current_difficulty!r} "
        f"ceiling={session.interview_difficulty!r} excluded_session={session_id}",
        flush=True,
    )

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
            f"[INTERVIEW-RAG] DB query table=common_interviewquestions "
            f"role={role!r} difficulty={current_difficulty!r} "
            f"top_k={top_k}",
            flush=True,
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
                iq.source_id,
                iq.embedding <=> %s::vector AS distance

            FROM common_interviewquestions iq

            WHERE LOWER(iq.role) = LOWER(%s)
              AND iq.difficulty = %s

            -- Don't retrieve questions already asked in this session
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
            current_difficulty,
            session_id,
            query_embedding,
            top_k,
        ))

        questions = cur.fetchall()
        print(f"[context_handler] Retrieved {len(questions)} question(s)", flush=True)
        print(f"[INTERVIEW-RAG] DB returned {len(questions)} candidate(s)", flush=True)
        for candidate in questions:
            print(
                f"[INTERVIEW-RAG] CANDIDATE id={candidate[0]} source_id={candidate[7]} "
                f"difficulty={candidate[5]!r} distance={candidate[8]} "
                f"question={candidate[1]!r}",
                flush=True,
            )

    # 5. No questions available
    if not questions and current_level > 0:
        with connection.cursor() as cur:
            cur.execute("""
                SELECT
                    iq.id, iq.question, iq.answer, iq.role, iq.experience,
                    iq.difficulty, iq.keywords,
                    iq.source_id,
                    iq.embedding <=> %s::vector AS distance
                FROM common_interviewquestions iq
                WHERE LOWER(iq.role) = LOWER(%s)
                AND iq.difficulty IN (%s)
                AND iq.id NOT IN (
                    SELECT question_id FROM common_askedquestions
                    WHERE session_id = %s
                )
                ORDER BY iq.embedding <=> %s::vector
                LIMIT %s;
            """, (
                query_embedding,
                role,
                "easy" if current_level == 1 else "medium",
                session_id,
                query_embedding,
                top_k,
            ))
            questions = cur.fetchall()
            print(
                f"[INTERVIEW-RAG] WIDENED query returned {len(questions)} candidate(s)",
                flush=True,
            )

    if not questions:
        print("[INTERVIEW-RAG] DB returned no unused question; using AI fallback", flush=True)
        question = _default_question(role, current_difficulty)
        session.question_count += 1
        session.save(update_fields=["question_count", "updated_at"])
        return {
            "status": "success",
            "role": role,
            "question": {
                "id": None,
                "question": question,
                "answer": "",
                "role": role,
                "experience": "any",
                "difficulty": current_difficulty,
                "keywords": [],
                "distance": None,
            },
            "generated": True,
        }

    # 6. Select the best retrieved question
    selected_question = questions[0]
    print(
        f"[INTERVIEW-RAG] SELECTED source=database id={selected_question[0]} "
        f"source_id={selected_question[7]} difficulty={selected_question[5]!r} "
        f"distance={selected_question[8]} question={selected_question[1]!r}",
        flush=True,
    )

    question_id = selected_question[0]
    # 7. Record ONLY the question actually asked
    print("[context_handler] Opening database connection to record asked question", flush=True)
    with connection.cursor() as cur:
        print(
            f"[INTERVIEW-RAG] RECORD asked_question session_id={session_id} "
            f"question_id={question_id}",
            flush=True,
        )

        cur.execute("""
            INSERT INTO common_askedquestions
                (session_id, question_id, asked_at)

            VALUES (%s, %s, NOW());
        """, (
            session_id,
            question_id
        ))
    print("[INTERVIEW-RAG] RECORD completed", flush=True)

    session.question_count += 1
    session.save(update_fields=["question_count", "updated_at"])

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
                "distance": selected_question[8],
                "source_id": selected_question[7],
        }
    }
    print(f"[context_handler] Returning response: {response}", flush=True)
    print("[context_handler] get_next_questions finished", flush=True)
    return response