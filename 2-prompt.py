import requests

model = "gemma3:12b-it-q4_K_M"
ollama_url = "http://10.3.5.132:11434/api/chat"

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
                    query: [要搜尋的內容]
                }
                }

                - 如果不需要調用工具或是無對應工具，請只回答純文字回應，不要輸出 JSON。
                """,
    }
]

messages.append({"role": "user", "content": "幫我搜尋看看川普最近又講了什麼狂言"})

payload = {"model": model, "messages": messages, "stream": False}

ai_message = (
    requests.post(ollama_url, json=payload).json().get("message", {}).get("content", "")
)

print(ai_message)
