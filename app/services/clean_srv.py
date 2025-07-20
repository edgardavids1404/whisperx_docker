import logging

import requests

from app.utils.config_loader import get_config

log = logging.getLogger(__name__)
config = get_config()


def clean_text(asr_text: str) -> str:
    prompt = f"""
### Instruction:
Clean and correct the following ASR-generated text:
1. Add appropriate punctuation.
2. Fix obvious recognition errors.
3. Preserve the original languages (Persian & English).
4. Keep the meaning intact.
5. Only write the cleaned text.

### Input Text:
{asr_text}

### Cleaned Text:
""".strip()

    payload = {
        "model": config["ollama"]["model"],
        "prompt": prompt.replace("\n", "\\n"),
        "stream": False,
    }

    r = requests.post(config["ollama"]["endpoint"], json=payload, timeout=300)
    r.raise_for_status()
    return r.json().get("response", "").strip()
