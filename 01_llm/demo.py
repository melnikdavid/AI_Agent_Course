from replay import Replay

model = Replay({"role": "assistant", "content": "Hello!"})
messages = [{"role": "user", "content": "Say hello"}]
print(model(messages)["content"])
