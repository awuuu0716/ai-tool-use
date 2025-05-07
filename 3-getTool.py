import json


def is_ai_call_tool_json(message: str) -> bool:
    try:
        data = json.loads(message)
        return data.get("call_tool", False)
    except json.JSONDecodeError:
        return False


# 工具定義
def google(query: str) -> str:
    # 等等再完成這個 function
    return ""


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
