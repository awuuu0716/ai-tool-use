import requests

model = "gemma3:12b-it-q4_K_M"
ollama_url = "http://10.3.5.132/llm/api/chat"

messages = [
    {
        "role": "system",
        "content": "Hello",
    }
]

payload = {"model": model, "messages": messages, "stream": False}

ai_message = (
    requests.post(ollama_url, json=payload).json().get("message", {}).get("content", "")
)

print(ai_message)
