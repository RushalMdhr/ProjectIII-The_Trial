
import sys

from .connection import get_db_cursor
sys.path.append(r'D:\Rushal\VS_code\Python\ProjectIII\backend')
from ai.utils.embeddings import embed_text_local

def relevant_context(user_query, top_k=5):
    """
    Retrieve relevant context from the database based on the user's query.
    
    Args:
        user_query (str): The user's input query.
        top_k (int): The number of top results to retrieve.
    
    Returns:
        list: A list of relevant context strings.
    """
    # Connect to the database
    with get_db_cursor() as cur:
        # Step 1: Generate embedding for the user query
        query_embedding = embed_text_local(user_query)
        
        if query_embedding is None:
            print("⚠️ Failed to generate embedding for the user query.")
            return []
        
        # Step 2: Retrieve relevant context from the database
        select_query = """
            SELECT question, answer, role, experience, difficulty, keywords
            FROM common_interviewquestions
            ORDER BY embedding <-> %s ::vector
            LIMIT 5
        """
        
        cur.execute(select_query, (query_embedding,))
        results = cur.fetchall()
        
        # Step 3: Format the results into a list of context strings
        context_list = []
        for row in results:
            question, answer, role, experience, difficulty, keywords = row
            context_str = f"Question: {question}\nIdeal_Answer: {answer}\nRole: {role}, Experience: {experience}, Difficulty: {difficulty}, Keywords: {keywords}"
            context_list.append(context_str)
        
        return context_list