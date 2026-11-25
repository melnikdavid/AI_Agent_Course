import os
import json
import httpx
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


# =====================================
# 1. Configuration
# =====================================

API_KEY = os.environ["LLM_API_KEY"]
BASE_URL = os.environ["LLM_BASE_URL"]
MODEL = os.environ["LLM_MODEL"]


# =====================================
# 2. Tools
# =====================================

def search(topic):
    database = {
        "python": "Python is a versatile programming language.",
        "java": "Java is a statically typed programming language.",
        "sql": "SQL is used to manage relational databases."
    }

    return database.get(
        topic.lower(),
        "No information found"
    )


def save_report(content):
    Path("report.txt").write_text(
        content,
        encoding="utf-8"
    )

    return "Report saved successfully"


# =====================================
# 3. Tool Registry
# =====================================

registry = {
    "search": search,
    "save_report": save_report
}


# =====================================
# 4. Tool Schemas
# =====================================

tools = [
    {
        "type": "function",
        "function": {
            "name": "search",
            "description": "Search the local knowledge base",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {"type": "string"}
                },
                "required": ["topic"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "save_report",
            "description": "Save a report to a local file",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {"type": "string"}
                },
                "required": ["content"],
                "additionalProperties": False
            }
        }
    }
]


# =====================================
# 5. LLM Client
# =====================================

def call_llm(messages):

    response = httpx.post(
        BASE_URL.rstrip("/") + "/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}"
        },
        json={
            "model": MODEL,
            "messages": messages,
            "tools": tools,
            "tool_choice": "auto"
        },
        timeout=30
    )

    response.raise_for_status()

    return response.json()["choices"][0]["message"]


# =====================================
# 6. Agent Execution Loop
# =====================================

def run_agent(task, max_steps=10):

    messages = [
        {
            "role": "system",
            "content": (
                "You are a research agent. "
                "Use the available tools to complete tasks. "
                "Base reports on search results. "
                "Do not invent information. "
                "Save reports only when requested."
            )
        },
        {
            "role": "user",
            "content": task
        }
    ]

    for step in range(max_steps):

        print(f"\n--- Step {step + 1} ---")

        # THINK
        message = call_llm(messages)

        messages.append(message)

        tool_calls = message.get("tool_calls")

        # STOP CONDITION
        if not tool_calls:
            return message.get("content")

        for tool_call in tool_calls:

            # IDENTIFY TOOL
            function = tool_call["function"]
            name = function["name"]

            print("Selected tool:", name)

            # ACT
            try:
                arguments = json.loads(
                    function["arguments"]
                )

                print("Arguments:", arguments)

                result = registry[name](**arguments)

            except (KeyError, TypeError, ValueError, OSError) as exc:
                result = f"Tool error: {exc}"

            print("Observation:", result)

            # OBSERVE - UPDATE CONTEXT
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "content": result
            })

    return "Maximum steps reached"


# =====================================
# 7. Main
# =====================================

if __name__ == "__main__":

    task = input("Enter your task: ")

    answer = run_agent(task)

    print("\nFinal answer:")
    print(answer)