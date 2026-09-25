import requests

_SESSION = requests.Session()
_SESSION.trust_env = False

def generate_with_ollama(model: str, prompt: str, temperature: float = 0.0) -> str:
    """
    Calls a local Ollama model.

    Requires Ollama running locally:
        ollama serve
        ollama pull qwen2.5:7b

    Args:
        model: Ollama model name, for example "qwen2.5:7b"
        prompt: Full prompt to send
        temperature: Sampling temperature

    Returns:
        Model response text
    """
    url = "http://127.0.0.1:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature
        }
    }

    try:
        response = _SESSION.post(url, json=payload, timeout=120)
        response.raise_for_status()
    except requests.exceptions.ConnectionError as exc:
        raise RuntimeError(
            "Could not connect to Ollama. Make sure Ollama is installed and running."
        ) from exc

    data = response.json()
    return data.get("response", "")
