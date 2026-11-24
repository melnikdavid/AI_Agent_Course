import os
from dotenv import load_dotenv


def config():
    load_dotenv()
    return {
        "url": os.environ["LLM_BASE_URL"].rstrip("/"),
        "model": os.environ["LLM_MODEL"],
        "key": os.environ["LLM_API_KEY"],
    }


import httpx


def chat(messages, tools=None):
    cfg = config()
    body = {"model": cfg["model"], "messages": messages}
    if tools:
        body["tools"] = tools
    response = httpx.post(
        cfg["url"] + "/chat/completions", json=body,
        headers={"Authorization": "Bearer " + cfg["key"]},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]
