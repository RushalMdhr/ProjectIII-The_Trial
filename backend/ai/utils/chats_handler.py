from ai.llm import ai


SYSTEM_PROMPT = """
You are a helpful, accurate, and reliable AI assistant.

Understand the user's intent, provide clear and practical answers,
and adapt your response to their needs.

Use the provided conversation history and context when relevant.

Be concise for simple questions and detailed when necessary.

Never fabricate information. If you are uncertain or the provided
context is insufficient, acknowledge that clearly.

Maintain a friendly and professional tone.
"""


def chats_handler(
    user_content,
    chat_history=None,
    context=None,
):
    """
    Prepare conversation context and generate an AI response.

    Args:
        user_content (str):
            Current user query.

        chat_history (list):
            Previous conversation messages.

        context (str):
            Retrieved RAG/context information.

    Returns:
        dict:
            {
                "user_content": str,
                "assistant_content": str
            }
    """

    chat_history = chat_history or []
    context = context or ""

    messages = []

    # -------------------------
    # System prompt
    # -------------------------
    syste

    # -------------------------
    # Retrieved context
    # -------------------------
    if context:
        messages.append({
            "role": "system",
            "content": (
                "Use the following context when it is relevant "
                "to answering the user's question.\n\n"
                f"CONTEXT:\n{context}"
            ),
        })

    # -------------------------
    # Previous chat history
    # -------------------------
    messages.extend(chat_history)

    # -------------------------
    # Current user query
    # -------------------------
    messages.append({
        "role": "user",
        "content": user_content,
    })

    # -------------------------
    # Generate response
    # -------------------------
    response = ai(msg=messages)

    assistant_content = response.message.content

    return {
        "user_content": user_content,
        "assistant_content": assistant_content,
    }