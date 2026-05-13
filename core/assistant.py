from typing import Optional, List, Dict, Any
from core.intent import classify_intent, guess_location
from core.style import natsumi
from core.memory import format_memory
from core.llm import generate_llm
from tools.weather import get_weather, outfit_recommendation
from tools.search import web_search, search_summary
from tools.coding import coding_search_summary


def simple_chat(message: str, memory: Optional[List[Dict[str, str]]] = None) -> str:
    """모델 파일이 없어도 일반 대화에 짧게 반응하는 경량 fallback."""
    m = (message or "").strip().lower()

    if any(x in m for x in ["안녕", "하이", "hello", "hi", "ㅎㅇ"]):
        return "안녕. 불렀으면 뭔가 물어봐. 딱히 기다린 건 아니지만 😾"

    if any(x in m for x in ["뭐해", "뭐 함", "뭐하", "심심", "놀자"]):
        return "지금은 네 질문 받을 준비 중이야. 날씨, 코딩, 검색, 잡담 정도는 바로 받아줄게 😼"

    if any(x in m for x in ["고마워", "감사", "땡큐", "thanks"]):
        return "흥, 별거 아니거든. 그래도 도움 됐다면 됐어 😼"

    if any(x in m for x in ["미안", "죄송"]):
        return "뭐… 알면 됐어. 다음엔 제대로 말해줘, 바보야 😾"

    if any(x in m for x in ["좋아", "좋네", "굿", "멋지", "대박"]):
        return "그치? 내가 좀 쓸만하긴 해. 너무 띄워주진 말고 😼"

    if any(x in m for x in ["힘들", "우울", "슬퍼", "아파", "지쳐", "불안"]):
        return "괜찮은 척하지 마. 지금은 물 한 모금 마시고, 해야 할 걸 하나만 작게 나눠보자. 내가 같이 정리해줄게 😿"

    if any(x in m for x in ["너 누구", "자기소개", "소개해", "정체"]):
        return "나는 나츠미야. 가볍게 돌아가는 AI 비서고, 날씨·검색·코딩·디스코드 봇 도움을 해줄 수 있어. 츤데레는 덤이야 😾"

    if any(x in m for x in ["뭘 할 수", "기능", "도움", "사용법"]):
        return "날씨, 옷 추천, 한강 온도, 코딩 오류, 웹검색, 디스코드 봇 연동을 도와줄 수 있어. 질문만 던져봐 😼"

    if "?" in message or "뭐" in m or "어떻게" in m or "왜" in m:
        return "그건 조금 더 구체적으로 말해줘. 예를 들면 '서울 날씨', 'discord.js 오류', '옷 추천'처럼 물어보면 바로 처리할게 😾"

    return f"응, '{message[:80]}' 말한 거지? 지금은 경량 대화 모드라 짧게 반응할게. 더 자세히 원하면 검색이나 코딩처럼 목적을 붙여줘 😼"


def answer(message: str, user_id="guest", location: Optional[str]=None, memory: Optional[List[Dict[str,str]]]=None) -> Dict[str, Any]:
    intent = classify_intent(message)
    if intent == "weather":
        loc = guess_location(message, location)
        data = get_weather(loc)
        if not data:
            return {"route": intent, "reply": natsumi("날씨를 못 찾겠어. 지역명을 다시 말해줘 😿")}
        reply = f"{data['location']} 현재 {data.get('desc') or '날씨 정보 없음'}, 기온 {data.get('temp_c')}°C, 체감 {data.get('feels_like_c')}°C, 습도 {data.get('humidity')}%, 바람 {data.get('wind_kmph')}km/h 정도야."
        return {"route": intent, "reply": natsumi(reply), "data": data}
    if intent == "water_temp":
        data = get_weather("서울")
        if not data:
            return {"route": intent, "reply": natsumi("한강 주변 날씨를 못 찾겠어. 수온도 확실히 말하기 어려워 😿")}
        reply = f"서울 한강 주변은 현재 {data.get('desc') or '날씨 정보 없음'}, 기온 {data.get('temp_c')}°C, 체감 {data.get('feels_like_c')}°C 정도야. 다만 한강 수온은 공식 관측값을 못 찾으면 확실하지 않아. 산책 기준이면 {outfit_recommendation(data)}"
        return {"route": intent, "reply": natsumi(reply), "data": data, "water_temp_confirmed": False}
    if intent == "outfit":
        data = get_weather(guess_location(message, location))
        if not data:
            return {"route": intent, "reply": natsumi("날씨값을 못 가져와서 옷 추천이 애매해 😾")}
        return {"route": intent, "reply": natsumi(f"{data['location']} 기준 기온 {data.get('temp_c')}°C, 체감 {data.get('feels_like_c')}°C야. {outfit_recommendation(data)}"), "data": data}
    if intent == "coding":
        reply, items = coding_search_summary(message)
        return {"route": intent, "reply": generate_llm(f"코딩 검색 결과를 짧게 요약해줘.\n{reply}", fallback=reply), "sources": items[:4]}
    if intent == "search":
        items = web_search(message, 4)
        if not items:
            return {"route": intent, "reply": natsumi("검색 결과를 못 가져왔어 😿")}
        summary = search_summary(message, items)
        return {"route": intent, "reply": generate_llm(f"검색 결과를 짧게 요약해줘.\n{summary}", fallback=summary), "sources": items[:4]}
    mem = format_memory(memory or [])
    fallback_reply = simple_chat(message, memory)
    return {"route": intent, "reply": generate_llm((f"이전 대화:\n{mem}\n\n" if mem else "") + f"사용자 질문: {message}", fallback=fallback_reply)}
