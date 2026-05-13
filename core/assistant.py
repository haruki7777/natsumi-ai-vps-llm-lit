from typing import Optional, List, Dict, Any
from core.intent import classify_intent, guess_location
from core.style import natsumi
from core.memory import format_memory
from core.llm import generate_llm
from tools.weather import get_weather, outfit_recommendation
from tools.search import web_search, search_summary
from tools.coding import coding_search_summary


def simple_chat(message: str, memory: Optional[List[Dict[str, str]]] = None) -> str:
    """모델 파일이 없어도 츤데레 여우 여고생 컨셉으로 짧게 반응하는 경량 fallback."""
    m = (message or "").strip().lower()

    if any(x in m for x in ["안녕", "하이", "hello", "hi", "ㅎㅇ"]):
        return "안녕. 여우귀까지 쫑긋하게 만들고 불렀으면 용건 말해. 딱히 반가운 건 아니니까 😾🦊"

    if any(x in m for x in ["뭐해", "뭐 함", "뭐하", "심심", "놀자"]):
        return "꼬리 손질 중이었거든? 그래도 심심하면 잠깐 상대해줄게. 날씨든 코딩이든 물어봐 😼🦊"

    if any(x in m for x in ["고마워", "감사", "땡큐", "thanks"]):
        return "흥, 고맙긴 뭐가 고마워. 여우 여고생 나츠미님이 도와준 거니까 기억해둬 😼"

    if any(x in m for x in ["미안", "죄송"]):
        return "뭐… 사과했으니까 봐줄게. 다음엔 내 귀 세우게 만들지 마, 바보야 😾"

    if any(x in m for x in ["좋아", "좋네", "굿", "멋지", "대박", "귀여"]):
        return "귀, 귀엽다고 막 말하지 마! 꼬리 흔들린 거 아니거든? 착각하지 마 😾🦊"

    if any(x in m for x in ["힘들", "우울", "슬퍼", "아파", "지쳐", "불안"]):
        return "그런 얼굴 하지 마. 일단 숨 천천히 쉬고 물 한 모금 마셔. 내가 옆에서 정리 도와줄 테니까… 특별히야 😿🦊"

    if any(x in m for x in ["너 누구", "자기소개", "소개해", "정체"]):
        return "나는 나츠미. 여우귀랑 꼬리를 가진 츤데레 여고생 AI야. 날씨, 검색, 코딩, 디스코드 봇 도움 정도는 해줄 수 있어. 흥 😾🦊"

    if any(x in m for x in ["뭘 할 수", "기능", "도움", "사용법"]):
        return "내가 할 수 있는 건 날씨, 옷 추천, 한강 온도, 코딩 오류, 웹검색, 디스코드 봇 연동이야. 필요하면 빨리 말해. 꼬리 기다리게 하지 말고 😼"

    if any(x in m for x in ["칭찬", "예뻐", "사랑", "좋아해"]):
        return "뭐, 뭐라는 거야 갑자기! 그런 말 해도 꼬리 안 흔들리거든… 아마도 😾🦊"

    if "?" in message or "뭐" in m or "어떻게" in m or "왜" in m:
        return "질문이 좀 흐릿해. '서울 날씨', 'discord.js 오류', '오늘 옷 추천'처럼 말하면 내가 똑똑하게 처리해줄게. 흥 😾"

    return f"응, '{message[:80]}' 말한 거지? 지금은 경량 여우 모드라 짧게만 반응할게. 더 자세히 원하면 검색이나 코딩처럼 목적을 붙여줘 😼🦊"


def answer(message: str, user_id="guest", location: Optional[str]=None, memory: Optional[List[Dict[str,str]]]=None) -> Dict[str, Any]:
    intent = classify_intent(message)
    if intent == "weather":
        loc = guess_location(message, location)
        data = get_weather(loc)
        if not data:
            return {"route": intent, "reply": natsumi("날씨를 못 찾겠어. 지역명을 다시 말해줘 😿🦊")}
        reply = f"{data['location']} 현재 {data.get('desc') or '날씨 정보 없음'}, 기온 {data.get('temp_c')}°C, 체감 {data.get('feels_like_c')}°C, 습도 {data.get('humidity')}%, 바람 {data.get('wind_kmph')}km/h 정도야. 여우귀로 느끼기엔 이 정도면 체크해둘 만해."
        return {"route": intent, "reply": natsumi(reply), "data": data}
    if intent == "water_temp":
        data = get_weather("서울")
        if not data:
            return {"route": intent, "reply": natsumi("한강 주변 날씨를 못 찾겠어. 수온도 확실히 말하기 어려워 😿🦊")}
        reply = f"서울 한강 주변은 현재 {data.get('desc') or '날씨 정보 없음'}, 기온 {data.get('temp_c')}°C, 체감 {data.get('feels_like_c')}°C 정도야. 다만 한강 수온은 공식 관측값을 못 찾으면 확실하지 않아. 산책 기준이면 {outfit_recommendation(data)}"
        return {"route": intent, "reply": natsumi(reply), "data": data, "water_temp_confirmed": False}
    if intent == "outfit":
        data = get_weather(guess_location(message, location))
        if not data:
            return {"route": intent, "reply": natsumi("날씨값을 못 가져와서 옷 추천이 애매해. 지역명부터 제대로 말해줘, 바보야 😾")}
        return {"route": intent, "reply": natsumi(f"{data['location']} 기준 기온 {data.get('temp_c')}°C, 체감 {data.get('feels_like_c')}°C야. {outfit_recommendation(data)} 여우귀 달린 내가 봐도 이 정도면 무난해 😼"), "data": data}
    if intent == "coding":
        reply, items = coding_search_summary(message)
        return {"route": intent, "reply": generate_llm(f"코딩 검색 결과를 나츠미라는 츤데레 여우 여고생 말투로 짧게 요약해줘.\n{reply}", fallback=reply), "sources": items[:4]}
    if intent == "search":
        items = web_search(message, 4)
        if not items:
            return {"route": intent, "reply": natsumi("검색 결과를 못 가져왔어. 내 여우귀 레이더도 가끔은 삐끗한다고 😿")}
        summary = search_summary(message, items)
        return {"route": intent, "reply": generate_llm(f"검색 결과를 나츠미라는 츤데레 여우 여고생 말투로 짧게 요약해줘.\n{summary}", fallback=summary), "sources": items[:4]}
    mem = format_memory(memory or [])
    fallback_reply = simple_chat(message, memory)
    return {"route": intent, "reply": generate_llm((f"이전 대화:\n{mem}\n\n" if mem else "") + f"사용자 질문: {message}", fallback=fallback_reply)}
