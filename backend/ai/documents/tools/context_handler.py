
from common.RAG_models import InterviewQuestions
from pgvector.django import CosineDistance
from ai.utils.embeddings import embed_text_local

def relevant_context(user_query, difficulty=None, top_k=1):
    """
    Retrieve relevant context from the database based on the user's query.
    
    Args:
        user_query (str): The user's input query.
        top_k (int): The number of top results to retrieve.
    
    Returns:
        list: A list of relevant context strings.
    """
    query_embedding = embed_text_local(user_query)
    if query_embedding is None:
        return []

    questions = InterviewQuestions.objects.exclude(
        embedding=None
    )
    if difficulty in {"easy", "medium", "hard"}:
        questions = questions.filter(difficulty=difficulty)

    questions = questions.annotate(
        distance=CosineDistance("embedding", query_embedding)
    ).order_by("distance")[:top_k]

    print(f"questions \n ===============\n {questions}",flush=True)
    return [
        {
            "id": question.id,
            "question": question.question,
            "ideal_answer": question.answer,
            "role": question.role,
            "experience": question.experience,
            "difficulty": question.difficulty,
            "keywords": question.keywords,
        }
        for question in questions
    ]