from replay import Replay, call
from tools import TOOLS
from progress import execute_plan

def answer(text):
    return {"role": "assistant", "content": text}

model = Replay(answer('{"steps":["Find solar"]}'),
    call("missing", '{}'), answer("Failed"),
    answer('{"steps":["Search local corpus"]}'),
    call("search", '{"query":"solar"}'), answer("R1/R4"))
for step in execute_plan("Research solar", model, TOOLS):
    print(step.status, step.goal)
