import json
from serpapi import GoogleSearch
import requests

SERPAPI_API_KEY = ""

model = "gemma3:12b-it-q4_K_M"
ollama_url = "http://10.3.5.132/ollama/api/chat"


def google(query: str) -> str:
    print(f"調用 google 搜尋: {query}")
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
        # print(f"is_ai_call_tool_json: {message}\n")
        data = json.loads(message)
        return data.get("call_tool", False)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}\n")
        return False


tool_map = {
    "google": google,
}


def handle_tool_call_json(message: str):
    data = json.loads(message)
    tool_name = data.get("tool_name", "")
    parameters = data.get("parameters", {})

    print(f"AI 想要調用工具:{tool_name} 參數:{parameters}\n")

    if tool_name in tool_map:
        tool_func = tool_map[tool_name]
        return tool_func(**parameters)
    else:
        return "(未知工具)"


messages = [
    {
        "role": "system",
        "content": """
                你是一個開發助手，會依據用戶需求調用工具。
                目前有 1 個工具:

                1. google 搜尋，整理用戶的需求，將需要搜尋的內容放入 query 參數: google

                請依照以下格式回覆：

                - 如果需要調用工具(例如說 google 搜尋)，請嚴格按照這個 JSON 格式輸出文字：
                {
                "call_tool": true,
                "tool_name": "google",
                "parameters": {
                    "query": [要搜尋的內容]
                }
                }

                - 如果不需要調用工具或是無對應工具，請只回答純文字回應，不要輸出 JSON。
                """,
    }
]

print("歡迎進入對話模式，輸入 'exit' 結束對話。\n")

while True:
    user_input = input("Input: ")

    if user_input.lower() == "exit":
        print("對話結束。\n")
        break

    messages.append({"role": "user", "content": user_input})

    payload = {"model": model, "messages": messages, "stream": False}

    response = requests.post(ollama_url, json=payload)

    reply = response.json().get("message", {}).get("content", "")

    # print(f"AI first reply: {reply}\n")

    if is_ai_call_tool_json(reply):
        reply = handle_tool_call_json(reply)

    print(f"AI: {reply}\n")

    # 加入 AI 回覆
    messages.append({"role": "assistant", "content": reply})
