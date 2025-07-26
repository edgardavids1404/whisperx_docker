import logging

import requests

from app.utils.config_loader import get_config

log = logging.getLogger(__name__)
config = get_config()


def clean_text(asr_text: str) -> str:
    prompt = f"""
### Role:
Edit ASR text in mixed Persian-English.

### Task:
Clean errors, keep meaning and language.

### Rules:

1. Add natural punctuation.
2. Fix Persian/English ASR mistakes.
3. Don’t translate.
4. Preserve intent.
5. Use [inaudible] for unclear parts.
6. Output only the cleaned text.
7. No added info—keep it natural.

### Input:
{asr_text}

### Output:
""".strip()

    payload = {
        "model": config["ollama"]["model"],
        "prompt": prompt.replace("\n", "\\n"),
        "stream": False,
    }

    r = requests.post(config["ollama"]["endpoint"], json=payload, timeout=300)
    r.raise_for_status()
    return r.json().get("response", "").strip()
