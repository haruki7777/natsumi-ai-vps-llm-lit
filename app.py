from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional
from core.assistant import answer
from core.memory import add_message, get_memory
from core.llm import generate_llm, llm_status

app = FastAPI(title="Natsumi AI VPS LLM Lit")

class AssistantRequest(BaseModel):
    user_id: str = Field(default="guest")
    message: str
    location: Optional[str] = None

class LLMRequest(BaseModel):
    message: str
    system: Optional[str] = None

@app.get("/")
def root():
    return {"name": "Natsumi AI VPS LLM Lit", "llm": llm_status()}

@app.get("/health")
def health():
    return {"status": "ok", "llm": llm_status()}

@app.post("/assistant")
def assistant(req: AssistantRequest):
    memory = get_memory(req.user_id)
    result = answer(req.message, user_id=req.user_id, location=req.location, memory=memory)
    add_message(req.user_id, "user", req.message)
    add_message(req.user_id, "assistant", result["reply"])
    return result

@app.post("/chat")
def chat(req: AssistantRequest):
    return assistant(req)

@app.post("/llm")
def llm(req: LLMRequest):
    return {"reply": generate_llm(req.message, system=req.system), "llm": llm_status()}
