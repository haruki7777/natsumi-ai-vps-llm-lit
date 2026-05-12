from tools.search import web_search

def coding_search_summary(query: str, language=None, max_results=4):
    q = f"{language + ' ' if language else ''}{query} official docs github stackoverflow latest"
    items = web_search(q, max_results=max_results)
    if not items:
        return ("코딩 검색 결과를 못 가져왔어. 에러 로그를 보내줘 😿", [])
    lines = [f"'{query}' 관련 자료를 찾았어."]
    for i, item in enumerate(items[:3], 1):
        lines.append(f"{i}. {item.get('title','제목 없음')} - {item.get('snippet','')} ({item.get('url','')})")
    return "\n".join(lines), items
