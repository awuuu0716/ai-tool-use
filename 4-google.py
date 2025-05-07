import json
from serpapi import GoogleSearch

SERPAPI_API_KEY = ""


def google(query: str) -> str:
    search = GoogleSearch({"q": query, "api_key": SERPAPI_API_KEY, "num": 3})
    results = search.get_dict()
    output = []

    for result in results.get("organic_results", []):
        title = result.get("title")
        link = result.get("link")
        output.append(f"title:{title} url:{link}")

    return "\n".join(output) if output else "(沒有搜尋結果)"


def is_ai_call_tool_json(message: str) -> bool:
    try:
        data = json.loads(message)
        return data.get("call_tool", False)
    except json.JSONDecodeError:
        return False


tool_map = {
    "google": google,
}


def handle_tool_call_json(message: str):
    data = json.loads(message)
    tool_name = data.get("tool_name", "")
    parameters = data.get("parameters", {})

    if tool_name in tool_map:
        tool_func = tool_map[tool_name]
        return tool_func(**parameters)
    else:
        return "(未知工具)"


res = google("川普 狂言 最近")

print(res)
