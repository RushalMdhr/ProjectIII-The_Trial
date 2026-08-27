from ai.models.llama import generate as llama_generate
from ai.models.qwen import generate as qwen_generate


def generate_response(prompt, model="llama"):
    if model == "llama":
        return llama_generate(prompt)

    if model == "qwen":
        return qwen_generate(prompt)

    raise ValueError("Unknown model")