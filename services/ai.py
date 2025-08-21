# services/ai.py
import os, json, time, requests
from dataclasses import dataclass
from typing import Optional

__all__ = ["generate_care_reply", "AIResult"]

SYSTEM_PROMPT = (
    "You are a supportive journaling companion. "
    "Be brief, kind, non-judgmental, give user a supportive answer and practical steps for support. "
    "Also rate the user's overall mood from 1 (very negative) to 10 (very positive). "
    "Respond ONLY as compact JSON with keys: reply (string), mood (integer 1-10). "
    "Example: {\"reply\":\"...\",\"mood\":7} "
    "Do not add any extra text. "
    "If the user only wants to write, acknowledge and do not analyze."
)

CRISIS_HINT = (
    "⚠️ If you ever feel in immediate danger or consider harming yourself, "
    "please reach out right away to a crisis hotline or local emergency services."
)
CRISIS_KEYWORDS = {"suicide", "kill myself", "self harm", "end my life"}

@dataclass
class AIResult:
    text: str
    mood: Optional[int] = None
    from_cache: bool = False

def _looks_like_crisis(user_text: str) -> bool:
    t = user_text.lower()
    return any(k in t for k in CRISIS_KEYWORDS)

def _retry(fn, retries=3, backoff=0.8):
    last_exc = None
    for i in range(retries):
        try:
            return fn()
        except Exception as e:
            last_exc = e
            time.sleep(backoff * (i + 1))
    raise last_exc

def _openai_completion(user_text: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY in .env")

    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text},
        ],
        "temperature": 0.6,
        "max_tokens": 350,
    }

    def go():
        r = requests.post(f"{base_url}/chat/completions", headers=headers, json=payload, timeout=30)
        r.raise_for_status()
        data = r.json()
        return data["choices"][0]["message"]["content"].strip()

    return _retry(go)

def generate_care_reply(user_text: str, respect_no_reply: bool = False) -> AIResult:
    if respect_no_reply:
        return AIResult(
            text="I respect that. If you just want to write freely, go ahead — I'm here if you ever want feedback.",
            mood=None
        )

    try:
        raw = _openai_completion(user_text)

        # Προσπάθησε να κάνεις parse το JSON. Αν δεν είναι καθαρό JSON, πάρε fallback.
        try:
            obj = json.loads(raw)
            reply = (obj.get("reply") or "").strip()
            mood = obj.get("mood")
        except Exception:
            reply = raw.strip()
            mood = None

        if isinstance(mood, (int, float)):
            mood = int(max(1, min(10, mood)))
        else:
            mood = None

        if _looks_like_crisis(user_text):
            reply = f"{CRISIS_HINT}\n\n{reply}"

        return AIResult(text=reply, mood=mood)

    except Exception:
        return AIResult(
            text=(
                "I couldn't reach the assistant right now. If you want, try again in a bit — "
                "and in the meantime, keep writing. I'm here for you. ❤️"
            ),
            mood=None
        )
