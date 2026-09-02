from .request_ollama import ollama_client

def embed_text(text, model="nomic-embed-text"):
    try:
        response = ollama_client.embeddings(model=model, prompt=text)
        return response['embedding']

    except Exception as e:
        print(f"Embedding error: {e}")
        return None