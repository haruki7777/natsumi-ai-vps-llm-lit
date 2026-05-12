import re
from core.config import ANSWER_STYLE

def clean(text):
    return re.sub(r"\s+", " ", text or "").strip()

def concise(text):
    text = clean(text)
    limit = 260 if ANSWER_STYLE == "tiny" else 420
    return text[:limit].rstrip() + "..." if len(text) > limit else text

def natsumi(text):
    text = concise(text) or "으으... 답변이 비었잖아 😾"
    if not any(x in text for x in ["😾", "😿", "😼", "흥"]):
        text += " 흥 😼"
    return text
