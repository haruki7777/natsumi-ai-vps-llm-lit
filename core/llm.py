import os, threading
from typing import Optional
from core.config import *
from core.style import natsumi

_llm = None
_llm_error = None
_lock = threading.Lock()
DEFAULT_SYSTEM = "너는 나츠미라는 한국어 AI 어시스턴트다. 컨셉은 여우귀와 꼬리가 있는 츤데레 여고생이다. 말투는 장난스럽고 살짝 툴툴대지만 다정하다. 답변은 짧고 실용적으로 한다. 확실하지 않은 정보는 지어내지 말고 확실하지 않다고 말한다. 이모지로 😾😼😿🦊를 가끔 사용한다."

def llm_status():
    return {"enabled": LLM_ENABLED, "loaded": _llm is not None, "model_path": LLM_MODEL_PATH, "model_exists": os.path.exists(LLM_MODEL_PATH), "n_ctx": LLM_N_CTX, "n_threads": LLM_N_THREADS, "max_tokens": LLM_MAX_TOKENS, "last_error": _llm_error}

def _load_llm():
    global _llm, _llm_error
    if not LLM_ENABLED:
        _llm_error = "LLM_ENABLED=false"
        return None
    if _llm is not None:
        return _llm
    if not os.path.exists(LLM_MODEL_PATH):
        _llm_error = f"model file not found: {LLM_MODEL_PATH}"
        return None
    with _lock:
        if _llm is not None:
            return _llm
        try:
            from llama_cpp import Llama
            _llm = Llama(model_path=LLM_MODEL_PATH, n_ctx=LLM_N_CTX, n_threads=LLM_N_THREADS, n_gpu_layers=0, use_mmap=True, use_mlock=False, verbose=False)
            _llm_error = None
            return _llm
        except Exception as e:
            _llm_error = f"{type(e).__name__}: {e}"
            return None

def _prompt(message, system=None):
    system = system or DEFAULT_SYSTEM
    return f"<|im_start|>system\n{system}<|im_end|>\n<|im_start|>user\n{message}<|im_end|>\n<|im_start|>assistant\n"

def generate_llm(message: str, system: Optional[str] = None, fallback: Optional[str] = None):
    llm = _load_llm()
    if llm is None:
        return natsumi(fallback or "작은 LLM 모델 파일이 없어. 그래도 날씨/검색/코딩은 처리할 수 있어 😿🦊")
    try:
        out = llm(_prompt(message, system), max_tokens=LLM_MAX_TOKENS, temperature=LLM_TEMPERATURE, top_p=LLM_TOP_P, stop=["<|im_end|>","<|endoftext|>"], echo=False)
        return natsumi(out["choices"][0]["text"].strip())
    except Exception as e:
        return natsumi(f"LLM 오류: {type(e).__name__}. 질문을 짧게 다시 보내봐 😿🦊")
