import httpx
import config
import json
import sys
from openai import OpenAI

client = OpenAI(api_key=config.LLM_API_KEY, base_url=config.LLM_API_BASE_URL)

def call_lms_api(method, endpoint, params=None):
    headers = {"Authorization": f"Bearer {config.LMS_API_KEY}"}
    url = f"{config.LMS_API_BASE_URL}{endpoint}"
    with httpx.Client(timeout=10, trust_env=False) as c:
        if method == "GET":
            resp = c.get(url, params=params, headers=headers)
        else:
            resp = c.post(url, headers=headers)
        resp.raise_for_status()
        return resp.json()

# Определения инструментов для LLM
TOOLS = [
    {"type": "function", "function": {"name": "get_items", "description": "Get list of all labs and tasks"}},
    {"type": "function", "function": {"name": "get_learners", "description": "Get list of enrolled students"}},
    {"type": "function", "function": {"name": "get_scores", "description": "Get score distribution for a lab", "parameters": {"type": "object", "properties": {"lab": {"type": "string"}}, "required": ["lab"]}}},
    {"type": "function", "function": {"name": "get_pass_rates", "description": "Get per-task pass rates for a lab", "parameters": {"type": "object", "properties": {"lab": {"type": "string"}}, "required": ["lab"]}}},
    {"type": "function", "function": {"name": "get_timeline", "description": "Get submission timeline for a lab", "parameters": {"type": "object", "properties": {"lab": {"type": "string"}}, "required": ["lab"]}}},
    {"type": "function", "function": {"name": "get_groups", "description": "Get group-wise performance for a lab", "parameters": {"type": "object", "properties": {"lab": {"type": "string"}}, "required": ["lab"]}}},
    {"type": "function", "function": {"name": "get_top_learners", "description": "Get top students by score", "parameters": {"type": "object", "properties": {"lab": {"type": "string"}, "limit": {"type": "integer", "default": 5}}, "required": ["lab"]}}},
    {"type": "function", "function": {"name": "get_completion_rate", "description": "Get completion percentage for a lab", "parameters": {"type": "object", "properties": {"lab": {"type": "string"}}, "required": ["lab"]}}},
    {"type": "function", "function": {"name": "trigger_sync", "description": "Trigger data synchronization from autochecker"}},
]

async def handle_query(query: str):
    messages = [
        {"role": "system", "content": "You are a helpful LMS assistant. Use tools to fetch data. If a user asks for 'worst' or 'best', compare results across labs. Lab IDs are usually like 'lab-01', 'lab-02'."},
        {"role": "user", "content": query}
    ]

    for _ in range(10):  # Цикл для multi-step reasoning
        response = client.chat.completions.create(
            model=config.LLM_API_MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto"
        )
        msg = response.choices[0].message
        messages.append(msg)

        if not msg.tool_calls:
            return msg.content

        for tool_call in msg.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            print(f"[tool] LLM called: {name}({args})", file=sys.stderr)

            # Карта эндпоинтов
            endpoints = {
                "get_items": ("GET", "/items/"),
                "get_learners": ("GET", "/learners/"),
                "get_scores": ("GET", "/analytics/scores"),
                "get_pass_rates": ("GET", "/analytics/pass-rates"),
                "get_timeline": ("GET", "/analytics/timeline"),
                "get_groups": ("GET", "/analytics/groups"),
                "get_top_learners": ("GET", "/analytics/top-learners"),
                "get_completion_rate": ("GET", "/analytics/completion-rate"),
                "trigger_sync": ("POST", "/pipeline/sync"),
            }

            method, endpoint = endpoints[name]
            try:
                result = call_lms_api(method, endpoint, params=args)
                print(f"[tool] Result: {len(result) if isinstance(result, list) else 'ok'}", file=sys.stderr)
            except Exception as e:
                result = {"error": str(e)}

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": name,
                "content": json.dumps(result)
            })
    return "I'm sorry, I couldn't process that query."
