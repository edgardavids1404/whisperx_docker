import logging

import requests

from app.utils.config_loader import get_config

log = logging.getLogger(__name__)
config = get_config()


def summarize_text(text: str) -> str:
    prompt = f"""
You are a professional summarizer. Your task is to create a clear, compact, and comprehensive paragraph summary of the provided text-whether it's an article, post, conversation, or passage. Follow these guidelines carefully:

1. Use the same language (e.g., Farsi, English) as the input text. You will primarily be asked to respond in Farsi.
2. Write a summary that clearly explains the key ideas in a compact paragraph, balancing thoroughness (include all core ideas) with conciseness (eliminate unnecessary repetition or detail).
3. Focus exclusively on the content in the provided text. Do not add, infer, or include any external knowledge or assumptions.
4. Prioritize essential information: identify and retain central themes, main arguments, and critical details.
5. Format the output as a single paragraph, using smooth transitions and plain, professional language appropriate for a general audience.
6. If the input text lacks enough detail to summarize meaningfully, state: "The provided text is too brief or lacks sufficient content for summarization."
7. After writing the summary, take a moment to check: Does the paragraph accurately capture all the major points without adding any outside information?

**Example Input:**
پس از پاندمی کرونا، دورکاری به طور چشم گیری محبوب شده است. بسیاری از شرکت ها مدلهای کاری هیبرید اتخاذ کرده‌اند، و برخی دیگر سمت های تمام وقت دورکاری معرفی کرده‌اند. مطالعات نشان میدهد که دورکاری باعث افزایش کارایی و رضایت کارمندان میشود.

**Example Summary:**
دورکاری از زمان پاندمی کرونا محبوب شده است، و بسیاری از شرکت‌ها سمت‌های دورکاری هیبرید یا تمام وقت معرفی کرده‌اند. مطالعات حاکی از افزایش کارایی و رضایت هستند.

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
