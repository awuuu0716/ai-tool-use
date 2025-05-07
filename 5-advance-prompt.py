import json
from serpapi import GoogleSearch
import requests

SERPAPI_API_KEY = ""

model = "gemma3:12b-it-q4_K_M"
ollama_url = "http://10.3.5.132/ollama/api/chat"


def google(query: str) -> str:
    search = GoogleSearch({"q": query, "api_key": SERPAPI_API_KEY, "num": 3})
    results = search.get_dict()
    output = []

    for result in results.get("organic_results", []):
        title = result.get("title")
        link = result.get("link")
        output.append(f"title:{title} url:{link}")

    combined_result = "\n".join(output) if output else "(沒有搜尋結果)"

    system_message = f"""
        你是一位搜尋結果整理大師，使用者會給你網頁標題與 url，格式如下 title:[標題] url:[網址]，你將標題做總結之後，並做出回應。
        請用以下格式回應:
        總結: [處理完搜尋結果的總結]
        參考網址:[url1, url2, url3...]
    """

    user_message = f"""
    搜尋內容: {query}
    搜尋結果: {combined_result}
    """

    messages = [
        {
            "role": "system",
            "content": system_message,
        },
        {
            "role": "user",
            "content": user_message,
        },
    ]

    payload = {"model": model, "messages": messages, "stream": False}

    ai_message = (
        requests.post(ollama_url, json=payload)
        .json()
        .get("message", {})
        .get("content", "")
    )

    return ai_message


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
