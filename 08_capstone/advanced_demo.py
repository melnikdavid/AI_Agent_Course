from advanced import advanced_research, BudgetExceeded
from replay import Replay, call
from policy import approve

def answer(text):
    return {"role":"assistant", "content":text}

model = Replay(answer('{"steps":["Search and save"]}'),
    call("search", '{"query":"solar"}'),
    call("save", '{"report":"Solar: R1/R4"}', "c2"),
    answer("Report written"))
try:
    for step in advanced_research("Research solar", model,
                                  "memory.db", approve):
        print(step.status, step.result)
except BudgetExceeded as exc:
    print("Stopped:", exc)
