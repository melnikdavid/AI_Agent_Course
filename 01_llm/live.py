from llm import chat

messages = [{"role": "user", "content": "Say hello"}]
print(chat(messages)["content"])
