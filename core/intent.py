from typing import Optional

WEATHER = ["날씨","기온","온도","비와","우산","춥","더워","습도","바람"]
WATER = ["수온","물온도","물 온도","강물","한강 온도","한강물","강 온도"]
OUTFIT = ["옷","입을까","코디","패션","외투","패딩","후드","뭐입"]
CODING = ["코드","에러","오류","python","파이썬","node","discord.js","자바","java","javascript","npm","fastapi","github","설치","버그","api"]
SEARCH = ["검색","블로그","후기","최신","요즘","알아봐","찾아","정보","추천","비교"]

def classify_intent(message: str):
    m = message.lower().replace(" ","")
    if any(w.replace(" ","") in m for w in WATER):
        return "water_temp"
    if any(w.replace(" ","") in m for w in OUTFIT):
        return "outfit"
    if any(w.replace(" ","") in m for w in WEATHER):
        return "weather"
    if any(w.lower().replace(" ","") in m for w in CODING):
        return "coding"
    if any(w.replace(" ","") in m for w in SEARCH):
        return "search"
    return "chat"

def guess_location(message: str, fallback: Optional[str] = None):
    if fallback:
        return fallback
    if "한강" in message:
        return "서울"
    for k in ["서울","부산","대구","인천","광주","대전","울산","제주","동대문구","답십리","강남","홍대"]:
        if k.lower() in message.lower():
            return k
    return "서울"
