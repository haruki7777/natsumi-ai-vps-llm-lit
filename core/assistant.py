from typing import Optional, List, Dict, Any
from core.intent import classify_intent, guess_location
from core.style import natsumi
from core.memory import format_memory
from core.llm import generate_llm
from tools.weather import get_weather, outfit_recommendation
from tools.search import web_search, search_summary
from tools.coding import coding_search_summary

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
    return {"route": intent, "reply": generate_llm((f"이전 대화:\n{mem}\n\n" if mem else "") + f"사용자 질문: {message}", fallback="모델 파일이 있으면 일반 대화도 가능해. 지금은 날씨/검색/코딩 중심으로 답할게.")}
