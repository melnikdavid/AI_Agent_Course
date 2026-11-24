from replay import Replay, call
from tools import TOOLS
from stateful import run_state

model = Replay(call("search", '{"query":"solar"}'),
               {"role":"assistant", "content":"R1/R4"})
s = run_state("Research solar", model, TOOLS)
print(s.status, s.turns, s.tool_calls, s.answer)
assert (s.status, s.turns, s.tool_calls) == ("completed", 2, 1)
