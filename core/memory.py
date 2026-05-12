from collections import defaultdict, deque
from core.config import MEMORY_MAX_MESSAGES

_memory = defaultdict(lambda: deque(maxlen=MEMORY_MAX_MESSAGES))

def add_message(user_id, role, content):
    _memory[user_id or "guest"].append({"role": role, "content": (content or "")[:500]})

def get_memory(user_id):
    return list(_memory[user_id or "guest"])

def format_memory(messages):
    return "\n".join([f"{m['role']}: {m['content']}" for m in messages[-4:]])
