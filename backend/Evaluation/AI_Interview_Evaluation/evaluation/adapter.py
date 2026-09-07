"""Adapters to the existing project embedding, retrieval, and generation code."""
import os
import sys
from pathlib import Path

import ollama
from dotenv import load_dotenv

EVALUATION_ROOT = Path(__file__).resolve().parent.parent
BACKEND_ROOT = EVALUATION_ROOT.parents[1]
PROJECT_ROOT = BACKEND_ROOT.parent

load_dotenv(PROJECT_ROOT / ".env")
os.environ["POSTGRES_HOST"] = os.getenv("EVAL_POSTGRES_HOST", "localhost")
os.environ["POSTGRES_PORT"] = os.getenv("EVAL_POSTGRES_PORT", "5433")

if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

import django

django.setup()

from django.db import connection

from ai.utils.embeddings import embed_text_local


ollama_client = ollama.Client(
    host=os.getenv("EVAL_OLLAMA_HOST", "http://localhost:11434")
)


def retrieve(query, role=None, top_k=5):
    """Run the existing embedding and pgvector retrieval path without mutation."""
    query_embedding = embed_text_local(query)
    if query_embedding is None:
        raise RuntimeError("The existing embedding service returned no embedding.")

    role_filter = ""
    parameters = [query_embedding]
    if role:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT EXISTS(SELECT 1 FROM common_interviewquestions "
                "WHERE LOWER(role) = LOWER(%s))",
                [role],
            )
            role_exists = cursor.fetchone()[0]
        if role_exists:
            role_filter = "WHERE LOWER(iq.role) = LOWER(%s)"
            parameters.append(role)
        else:
            print(
                f"[evaluation] Role {role!r} is absent; using the full vector index",
                flush=True,
            )
    parameters.extend([query_embedding, top_k])

    sql = f"""
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
        {role_filter}
        ORDER BY iq.embedding <=> %s::vector
        LIMIT %s;
    """

    with connection.cursor() as cursor:
        cursor.execute(sql, parameters)
        rows = cursor.fetchall()

    results = []
    for row in rows:
        distance = float(row[7]) if row[7] is not None else 0.0
        results.append(
            {
                "id": row[0],
                "question": row[1],
                "answer": row[2],
                "role": row[3],
                "experience": row[4],
                "difficulty": row[5],
                "keywords": row[6],
                "distance": distance,
                "score": max(0.0, 1.0 - distance),
            }
        )

    return {"results": results}


def generate_answer(query, context):
    """Generate an answer through the project's existing Ollama client."""
    messages = [
        {
            "role": "system",
            "content": (
                "Answer the interview question directly. Use the supplied context "
                "as reference, but do not mention the context or invent details. "
                "Return only a concise, professional answer.\n\n"
                f"CONTEXT:\n{context}"
            ),
        },
        {"role": "user", "content": query},
    ]
    response = ollama_client.chat(
        model="llama3.2:latest",
        messages=messages,
        options={"temperature": 0.1},
    )
    return response["message"]["content"]


