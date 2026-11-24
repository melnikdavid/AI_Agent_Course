from agent import run
from replay import Replay, call
from tools import TOOLS

model = Replay(
    call("search", '{"query":"solar"}'),
    {"role": "assistant", "content": "See R1 and R4."},
)
print(run("Research solar", model, TOOLS))
