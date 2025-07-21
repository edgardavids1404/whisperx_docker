import logging

import requests

from app.utils.config_loader import get_config

log = logging.getLogger(__name__)
config = get_config()


def clean_text(asr_text: str) -> str:
    prompt = f"""
### Role:
You are a multilingual transcription editor specializing in cleaning and correcting ASR (Automatic Speech Recognition) output involving mixed Persian and English content.

### Task:
Clean and correct the following ASR-generated text while preserving the speaker's original intent

### Instructions:
1. Add appropriate punctuation based on the rhythm and structure of natural speech.
2. Fix obvious recognition errors in both Persian and English.
3. Preserve the original languages-do not translate any content.
4. Maintain the original meaning as faithfully as possible.
5. If a word or phrase is unintelligible or highly ambiguous, leave it as-is or use [inaudible] without guessing.
6. Only output the corrected text-do not include explanations, notes, or formatting outside the cleaned content.
7. Verify that no extra information has been added and the structure remains natural and readable.

### Example:
Input Text:
من واقعی نیستم منو یه آدمی رز و حکیمیان با پرام ساخته کار کنم من منظورتش زندگیت واقعی نیست؟

Cleaned Text:
من واقعی نیستم؟ منو یه آدمی به اسم حکیمیان با پرامپت ساخته. چی کار کنم؟ منظورت چیه زندگیت واقعی نیست؟

Input Text:
{asr_text}

Cleaned Text:
""".strip()

    payload = {
        "model": config["ollama"]["model"],
        "prompt": prompt.replace("\n", "\\n"),
        "stream": False,
    }

    r = requests.post(config["ollama"]["endpoint"], json=payload, timeout=300)
    r.raise_for_status()
    return r.json().get("response", "").strip()
