from ai.utils.request_ollama import ollama_client

def ai(msg,model="llama3.2:latest",tools='auto'):
    return ollama_client.chat(
            model=model,
            messages=msg,
            options={
                "temperature": 0.1,      # Creative but not wild
                # "top_p": 0.9,            # Standard
                # "num_predict": 200,      # Short story (~200 tokens)
                # "num_ctx": 4096,         # Enough for context
                # "repeat_penalty": 1.1,   # Avoid repetition
                # "seed": 123,             # Reproducible
                # "mirostat": 1            # Adaptive creativity
            }

            )