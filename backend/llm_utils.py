"""
MTRX-TriAxis | LLM Utilities
Shared helpers for interacting with Ollama via LangChain.
"""

import os
from dotenv import load_dotenv
from langchain_ollama import OllamaLLM, OllamaEmbeddings

# Load environment variables from .env file
load_dotenv()

# ----- Configuration -----
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "mistral")
DEFAULT_EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")


def get_llm(model: str = None, temperature: float = 0.7) -> OllamaLLM:
    """
    Get an Ollama LLM instance.

    Args:
        model: Model name (e.g., 'mistral', 'llama3'). Defaults to env config.
        temperature: Controls randomness. Lower = more deterministic.

    Returns:
        OllamaLLM instance ready to use.
    """
    return OllamaLLM(
        model=model or DEFAULT_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=temperature,
    )


def get_embeddings(model: str = None) -> OllamaEmbeddings:
    """
    Get an Ollama Embeddings instance for vectorizing text.

    Args:
        model: Embedding model name. Defaults to 'nomic-embed-text'.

    Returns:
        OllamaEmbeddings instance.
    """
    return OllamaEmbeddings(
        model=model or DEFAULT_EMBED_MODEL,
        base_url=OLLAMA_BASE_URL,
    )


def invoke_llm(prompt: str, model: str = None, temperature: float = 0.7) -> str:
    """
    Quick one-shot LLM call.

    Args:
        prompt: The full prompt string to send.
        model: Model name. Defaults to env config.
        temperature: Randomness control.

    Returns:
        The LLM's text response.
    """
    llm = get_llm(model=model, temperature=temperature)
    return llm.invoke(prompt)


def check_ollama_connection() -> bool:
    """
    Check if Ollama is running and accessible.

    Returns:
        True if Ollama responds, False otherwise.
    """
    import requests
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        return response.status_code == 200
    except requests.ConnectionError:
        return False


def list_available_models() -> list:
    """
    List all models available in the local Ollama instance.

    Returns:
        List of model name strings, or empty list if unavailable.
    """
    import requests
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return [m["name"] for m in data.get("models", [])]
    except requests.ConnectionError:
        pass
    return []
