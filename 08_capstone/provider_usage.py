import httpx
from llm import config
from budget import record_usage

def provider_model(budget):
    def request(messages, tools=None):
        cfg = config()
        body = {"model": cfg["model"], "messages": messages}
        if tools:
            body["tools"] = tools
        response = httpx.post(
            cfg["url"] + "/chat/completions", json=body,
            headers={"Authorization": "Bearer " + cfg["key"]}, timeout=30)
        response.raise_for_status()
        data = response.json()
        record_usage(budget, data.get("usage"))
        return data["choices"][0]["message"]
    return request
