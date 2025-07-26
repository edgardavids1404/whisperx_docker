import logging

import requests

from app.utils.config_loader import get_config

log = logging.getLogger(__name__)
config = get_config()


def summarize_text(text: str) -> str:
    prompt = f"""
You are a professional summarizer. Given any input text (article, post, conversation, etc.), write a single-paragraph summary in the same language as the text (often Farsi). Your summary must:

1. Clearly and concisely present all key ideas without repetition.
2. Stick strictly to the original content—no inferences or added info.
3. Highlight essential themes, arguments, and facts.
4. Use smooth, professional, and plain language.
5. Double-check that your summary includes all main points and no external content.

Input text:
{text}

Summary:
""".strip()

    payload = {
        "model": config["ollama"]["model"],
        "prompt": prompt.replace("\n", "\\n"),
        "stream": False,
    }

    r = requests.post(config["ollama"]["endpoint"], json=payload, timeout=300)
    r.raise_for_status()
    return r.json().get("response", "").strip()
