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

Discord 봇에서 호출해서 쓰는 **경량 나츠미 AI API 서버**입니다.

나츠미는 **츤데레 여우 여고생 컨셉**의 AI 어시스턴트입니다.  
작은 GGUF LLM을 선택적으로 붙일 수 있고, 모델 파일이 없어도 날씨/한강 온도/검색/코딩/일반 짧은 대화는 기본 동작합니다.

---

## 🔗 주소

### GitHub Repository

```txt
https://github.com/haruki7777/natsumi-ai-vps-llm-lit
```

### Hugging Face Space

```txt
https://huggingface.co/spaces/haruki7777/natsumi-ai-vps-llm-lit
```

### API Base URL

```txt
https://haruki7777-natsumi-ai-vps-llm-lit.hf.space
```

Discord 봇이나 외부 앱에서는 이 주소를 `NATSUMI_API_URL`로 넣으면 됩니다.

```env
NATSUMI_API_URL=https://haruki7777-natsumi-ai-vps-llm-lit.hf.space
```

---

## 🧩 구조

```txt
Discord Bot / Web / App
        ↓ HTTP POST
Natsumi AI API Server
        ↓
Intent Router
  ├─ 일반 대화
  ├─ 날씨
  ├─ 한강 온도
  ├─ 옷 추천
  ├─ 검색
  ├─ 코딩 검색
  └─ 작은 LLM 선택 호출
```

---

## ✅ 상태 확인 API

### 요청

```bash
curl https://haruki7777-natsumi-ai-vps-llm-lit.hf.space/health
```

### 응답 예시

```json
{
  "status": "ok",
  "llm": {
    "enabled": true,
    "loaded": false,
    "model_path": "models/qwen2.5-0.5b-instruct-q4.gguf",
    "model_exists": false,
    "n_ctx": 768,
    "n_threads": 1,
    "max_tokens": 120,
    "last_error": null
  }
}
```

의미:

```txt
status: ok          → 서버 실행 중
model_exists: true → GGUF 모델 파일 있음
loaded: true        → 모델이 메모리에 로딩됨
loaded: false       → 아직 모델 호출 전이거나 모델 파일 없음
```

---

## 💬 메인 API: /assistant

일반적으로 디스코드 봇에서는 이 API만 쓰면 됩니다.

### Endpoint

```txt
POST /assistant
```

### Body

```json
{
  "user_id": "discord-user-id",
  "message": "안녕 나츠미",
  "location": "서울"
}
```

| 필드 | 필수 | 설명 |
|---|---:|---|
| `user_id` | 선택 | 사용자 구분용 ID. 디스코드 유저 ID를 넣으면 좋음 |
| `message` | 필수 | 사용자가 보낸 질문 |
| `location` | 선택 | 기본 위치. 날씨/옷추천에 사용 |

---

## 💬 /assistant 사용 예시

### curl

```bash
curl -X POST "https://haruki7777-natsumi-ai-vps-llm-lit.hf.space/assistant" \
-H "Content-Type: application/json" \
-d '{"user_id":"test","message":"안녕 나츠미"}'
```

응답 예시:

```json
{
  "route": "chat",
  "reply": "안녕. 여우귀까지 쫑긋하게 만들고 불렀으면 용건 말해. 딱히 반가운 건 아니니까 😾🦊"
}
```

---

## 🌤️ 날씨 질문 예시

### 요청

```bash
curl -X POST "https://haruki7777-natsumi-ai-vps-llm-lit.hf.space/assistant" \
-H "Content-Type: application/json" \
-d '{"user_id":"test","message":"지금 서울 날씨 어때"}'
```

### 응답 예시

```json
{
  "route": "weather",
  "reply": "서울 현재 맑음, 기온 18°C, 체감 18°C, 습도 60%, 바람 7km/h 정도야. 여우귀로 느끼기엔 이 정도면 체크해둘 만해. 흥 😼",
  "data": {
    "location": "서울",
    "temp_c": "18",
    "feels_like_c": "18",
    "humidity": "60",
    "wind_kmph": "7",
    "source": "wttr.in"
  }
}
```

날씨는 API 키 없이 `wttr.in` 기반으로 가져옵니다.

---

## 🌊 한강 온도 질문 예시

### 요청

```bash
curl -X POST "https://haruki7777-natsumi-ai-vps-llm-lit.hf.space/assistant" \
-H "Content-Type: application/json" \
-d '{"user_id":"test","message":"서울 한강 온도는 어때"}'
```

### 응답 예시

```json
{
  "route": "water_temp",
  "reply": "서울 한강 주변은 현재 맑음, 기온 18°C, 체감 18°C 정도야. 다만 한강 수온은 공식 관측값을 못 찾으면 확실하지 않아. 산책 기준이면 맨투맨이나 얇은 니트, 가벼운 자켓이면 좋아. 흥 😼",
  "water_temp_confirmed": false
}
```

주의:

```txt
'한강 온도'는 주변 기온과 실제 수온이 다릅니다.
이 서버는 공식 수온 관측값이 없으면 수온을 지어내지 않고,
서울/한강 주변 기온과 체감온도를 기준으로 안내합니다.
```

---

## 👕 옷 추천 예시

### 요청

```bash
curl -X POST "https://haruki7777-natsumi-ai-vps-llm-lit.hf.space/assistant" \
-H "Content-Type: application/json" \
-d '{"user_id":"test","message":"오늘 서울 옷 뭐 입을까"}'
```

### 응답 예시

```json
{
  "route": "outfit",
  "reply": "서울 기준 기온 18°C, 체감 18°C야. 맨투맨이나 얇은 니트, 가벼운 자켓이면 좋아. 여우귀 달린 내가 봐도 이 정도면 무난해 😼"
}
```

---

## 🔎 검색 질문 예시

### 요청

```bash
curl -X POST "https://haruki7777-natsumi-ai-vps-llm-lit.hf.space/assistant" \
-H "Content-Type: application/json" \
-d '{"user_id":"test","message":"요즘 디스코드 봇 호스팅 추천 검색해줘"}'
```

### 응답 형태

```json
{
  "route": "search",
  "reply": "검색 결과를 짧게 요약해서 알려줍니다.",
  "sources": [
    {
      "title": "검색 결과 제목",
      "url": "https://example.com",
      "snippet": "검색 결과 요약"
    }
  ]
}
```

검색은 API 키 없이 `ddgs` 기반으로 동작합니다. 검색엔진이 막히면 실패할 수 있습니다.

---

## 💻 코딩 질문 예시

### 요청

```bash
curl -X POST "https://haruki7777-natsumi-ai-vps-llm-lit.hf.space/assistant" \
-H "Content-Type: application/json" \
-d '{"user_id":"test","message":"discord.js 버튼 인터랙션 코드 알려줘"}'
```

### 응답 형태

```json
{
  "route": "coding",
  "reply": "코딩 검색 결과와 핵심 해결 방향을 짧게 알려줍니다.",
  "sources": []
}
```

공식 문서/GitHub/StackOverflow 쪽을 우선 검색하도록 구성되어 있습니다.

---

## 🧠 작은 LLM API: /llm

작은 GGUF 모델 파일이 있을 때 직접 LLM만 호출할 수 있습니다.

### 요청

```bash
curl -X POST "https://haruki7777-natsumi-ai-vps-llm-lit.hf.space/llm" \
-H "Content-Type: application/json" \
-d '{"message":"나츠미 자기소개해줘"}'
```

### 응답 예시

```json
{
  "reply": "나는 나츠미. 여우귀랑 꼬리를 가진 츤데레 여고생 AI야. 날씨, 검색, 코딩 정도는 도와줄 수 있어. 흥 😾🦊",
  "llm": {
    "enabled": true,
    "loaded": true
  }
}
```

모델 파일이 없으면 fallback 응답이 나옵니다.

---

## 🧠 모델 다운로드

Space나 VPS 터미널에서 실행:

```bash
python scripts/download_model.py
```

기본 모델:

```txt
Qwen/Qwen2.5-0.5B-Instruct-GGUF
```

기본 저장 위치:

```txt
models/qwen2.5-0.5b-instruct-q4.gguf
```

모델 파일이 없어도 아래 기능은 동작합니다.

```txt
일반 짧은 대화
날씨
한강 주변 온도
옷 추천
검색
코딩 검색
```

---

## 🐍 Python에서 API 쓰기

```python
import requests

API_URL = "https://haruki7777-natsumi-ai-vps-llm-lit.hf.space"

res = requests.post(
    f"{API_URL}/assistant",
    json={
        "user_id": "python-user",
        "message": "서울 한강 온도는 어때"
    },
    timeout=90
)

print(res.json()["reply"])
```

---

## ☕ Java에서 API 쓰기

Java 17 이상 기준입니다.

```java
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;

public class Main {
    public static void main(String[] args) throws Exception {
        String apiUrl = "https://haruki7777-natsumi-ai-vps-llm-lit.hf.space";
        String json = "{\"user_id\":\"java-user\",\"message\":\"서울 한강 온도는 어때\"}";

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(apiUrl + "/assistant"))
                .header("Content-Type", "application/json; charset=utf-8")
                .POST(HttpRequest.BodyPublishers.ofString(json, StandardCharsets.UTF_8))
                .build();

        HttpClient client = HttpClient.newHttpClient();
        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

        System.out.println(response.body());
    }
}
```

---

## 🟦 Discord.js에서 쓰기

```js
import axios from "axios";

const NATSUMI_API_URL = "https://haruki7777-natsumi-ai-vps-llm-lit.hf.space";

const res = await axios.post(`${NATSUMI_API_URL}/assistant`, {
  user_id: interaction.user.id,
  message: "서울 한강 온도는 어때",
});

await interaction.reply(res.data.reply);
```

명령어 예시는 여기에 있습니다.

```txt
discord-examples/discordjs/natsumi-command.js
```

---

## 🐍 discord.py에서 쓰기

예시 파일:

```txt
discord-examples/python-bot.py
```

필요 패키지:

```bash
pip install discord.py aiohttp
```

환경변수:

```env
DISCORD_TOKEN=디스코드_봇_토큰
NATSUMI_API_URL=https://haruki7777-natsumi-ai-vps-llm-lit.hf.space
```

---

## ☕ Java JDA에서 쓰기

예시 폴더:

```txt
discord-examples/java-jda/
```

환경변수:

```env
DISCORD_TOKEN=디스코드_봇_토큰
NATSUMI_API_URL=https://haruki7777-natsumi-ai-vps-llm-lit.hf.space
```

실행 예시:

```bash
cd discord-examples/java-jda
mvn exec:java -Dexec.mainClass=com.natsumi.bot.NatsumiJdaBot
```

---

## ⚙️ 권장 환경변수

저사양 Space/VPS용:

```env
LLM_ENABLED=true
LLM_N_CTX=768
LLM_N_THREADS=1
LLM_MAX_TOKENS=120
ANSWER_STYLE=tiny
```

조금 여유 있는 VPS용:

```env
LLM_ENABLED=true
LLM_N_CTX=1024
LLM_N_THREADS=2
LLM_MAX_TOKENS=180
ANSWER_STYLE=short
```

---

## 🦊 나츠미 컨셉

```txt
이름: 나츠미
컨셉: 여우귀 + 꼬리 + 츤데레 여고생 AI
말투: 장난스럽고 살짝 툴툴대지만 다정함
응답: 짧고 실용적
이모지: 😾 😼 😿 🦊
```

---

## ⚠️ 주의

- Hugging Face 무료 Space는 잠들 수 있어 첫 응답이 느릴 수 있습니다.
- 모델 파일이 없으면 LLM 일반 생성은 제한됩니다.
- 날씨는 `wttr.in`, 검색은 `ddgs` 기반이라 외부 서비스 상태에 따라 실패할 수 있습니다.
- 중요한 정보는 반드시 원문/공식 자료를 함께 확인하세요.
