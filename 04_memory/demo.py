from memory import init, remember, recent, with_memory
from agent import run
from replay import Replay, call
from tools import TOOLS

init("memory.db")
remember("memory.db", "Prefer concise reports")
print(recent("memory.db")[0])
model = Replay(call("search", '{"query":"solar"}'),
               {"role": "assistant", "content": "See R1/R4."})
print(run(with_memory("Research solar", "memory.db"), model, TOOLS))
