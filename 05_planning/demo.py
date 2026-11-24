from planner import make_plan, planned_task
from agent import run
from replay import Replay, call
from tools import TOOLS

model = Replay({"role": "assistant", "content":
                '{"steps":["Search solar","Report findings"]}'},
               call("search", '{"query":"solar"}'),
               {"role": "assistant", "content": "See R1/R4."})
plan = make_plan(model, "Research solar")
print(plan.steps)
print(run(planned_task("Research solar", plan), model, TOOLS))
