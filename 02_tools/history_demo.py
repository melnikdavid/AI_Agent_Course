from conversation import ask
from replay import Replay

model = Replay({"role": "assistant", "content": "Noted"},
               {"role": "assistant", "content": "Solar"})
history = []
print(ask(model, history, "My topic is solar"))
print(ask(model, history, "What is my topic?"))
print(len(history))
