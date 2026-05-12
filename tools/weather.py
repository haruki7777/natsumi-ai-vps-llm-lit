from typing import Optional, Dict, Any
import requests
from core.cache import get_cache, set_cache

ALIASES = {"서울":"Seoul","한강":"Seoul","서울 한강":"Seoul","부산":"Busan","대구":"Daegu","인천":"Incheon","제주":"Jeju","동대문구":"Dongdaemun-gu,Seoul","답십리":"Dapsimni,Seoul"}

def get_weather(location: str) -> Optional[Dict[str, Any]]:
    loc = ALIASES.get(location, location)
    key = f"weather:{loc}"
    cached = get_cache(key)
    if cached:
        return cached
    try:
        r = requests.get(f"https://wttr.in/{loc}", params={"format":"j1","lang":"ko"}, headers={"User-Agent":"curl/8.0"}, timeout=8)
        r.raise_for_status()
        data = r.json()
        cur = (data.get("current_condition") or [{}])[0]
        try:
            desc = (cur.get("lang_ko") or cur.get("weatherDesc") or [{}])[0].get("value")
        except Exception:
            desc = None
        result = {"location": location, "temp_c": cur.get("temp_C"), "feels_like_c": cur.get("FeelsLikeC"), "humidity": cur.get("humidity"), "wind_kmph": cur.get("windspeedKmph"), "desc": desc, "precip_mm": cur.get("precipMM"), "source": "wttr.in"}
        set_cache(key, result)
        return result
    except Exception:
        return None

def _float(v):
    try:
        return float(v)
    except Exception:
        return None

def outfit_recommendation(weather: Dict[str, Any]) -> str:
    feel = _float(weather.get("feels_like_c") or weather.get("temp_c"))
    if feel is None:
        return "얇은 겉옷 하나 챙기는 쪽이 안전해."
    if feel <= 0:
        return "롱패딩이나 두꺼운 패딩이 필요해."
    if feel <= 7:
        return "패딩이나 두꺼운 코트가 좋아."
    if feel <= 13:
        return "자켓, 가디건, 후드에 긴바지가 무난해."
    if feel <= 20:
        return "맨투맨이나 얇은 니트, 가벼운 자켓이면 좋아."
    if feel <= 27:
        return "반팔에 얇은 셔츠나 가벼운 겉옷 정도면 충분해."
    return "반팔, 얇은 바지, 통풍 좋은 옷으로 가."
