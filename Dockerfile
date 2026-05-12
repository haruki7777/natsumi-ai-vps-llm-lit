FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=7860
ENV LLM_ENABLED=true
ENV LLM_MODEL_PATH=models/qwen2.5-0.5b-instruct-q4.gguf
ENV LLM_N_CTX=768
ENV LLM_N_THREADS=1
ENV LLM_MAX_TOKENS=120
ENV ANSWER_STYLE=tiny
ENV CACHE_TTL_SECONDS=600
ENV MEMORY_MAX_MESSAGES=8

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
