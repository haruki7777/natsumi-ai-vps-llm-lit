from typing import List, Dict, Any
try:
    from ddgs import DDGS
except Exception:
    DDGS = None

def web_search(query: str, max_results=4, fetch_pages=True) -> List[Dict[str, Any]]:
    if DDGS is None:
        return []
    out = []
    try:
        with DDGS() as ddgs:
            for item in ddgs.text(query, region="kr-kr", safesearch="moderate", max_results=max_results):
                url = item.get("href") or item.get("url") or ""
                if url:
                    out.append({"title": item.get("title",""), "url": url, "snippet": item.get("body","")})
    except Exception:
        return []
    return out

def search_summary(query, items):
    if not items:
        return "검색 결과를 못 가져왔어 😿"
    lines = [f"'{query}' 검색 결과야."]
    for i, x in enumerate(items[:3], 1):
        lines.append(f"{i}. {x.get('title','제목 없음')} - {x.get('snippet','')} ({x.get('url','')})")
    return "\n".join(lines)
