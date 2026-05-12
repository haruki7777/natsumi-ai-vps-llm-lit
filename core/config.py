import os

LLM_ENABLED = os.getenv("LLM_ENABLED", "true").lower() == "true"
LLM_MODEL_PATH = os.getenv("LLM_MODEL_PATH", "models/qwen2.5-0.5b-instruct-q4.gguf")
LLM_N_CTX = int(os.getenv("LLM_N_CTX", "768"))
LLM_N_THREADS = int(os.getenv("LLM_N_THREADS", "1"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "120"))
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))
LLM_TOP_P = float(os.getenv("LLM_TOP_P", "0.9"))
ANSWER_STYLE = os.getenv("ANSWER_STYLE", "tiny")
CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "600"))
MEMORY_MAX_MESSAGES = int(os.getenv("MEMORY_MAX_MESSAGES", "8"))
