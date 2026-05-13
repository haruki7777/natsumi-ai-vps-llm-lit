---
title: Natsumi AI VPS LLM Lit
emoji: 🦊
colorFrom: yellow
colorTo: pink
sdk: docker
app_port: 7860
pinned: false
license: apache-2.0
---

# 🦊 Natsumi AI VPS LLM Lit

Discord 봇에서 호출해서 쓰는 경량 나츠미 AI 서버입니다.

## 구조

```txt
Hugging Face Space / VPS
  ├─ FastAPI AI 서버
  ├─ 작은 GGUF LLM 선택 로딩
  ├─ 날씨 / 한강 온도 / 검색 / 코딩 라우터
  └─ Discord 봇에서 HTTP 호출
```

## 엔드포인트

- `GET /health`
- `POST /assistant`
- `POST /chat`
- `POST /llm`

## 테스트

```bash
curl -X POST http://127.0.0.1:7860/assistant \
-H "Content-Type: application/json" \
-d '{"user_id":"test","message":"서울 한강 온도는 어때"}'
```

## Discord 봇 호출

Python, Java JDA, Discord.js 예시는 `discord-examples/` 폴더를 참고하세요.

## 저사양 권장 환경변수

```env
LLM_ENABLED=true
LLM_N_CTX=768
LLM_N_THREADS=1
LLM_MAX_TOKENS=120
ANSWER_STYLE=tiny
```

## 모델 다운로드

Space나 VPS 터미널에서:

```bash
python scripts/download_model.py
```

모델 파일이 없어도 날씨/검색/코딩 라우터는 기본 동작합니다.
