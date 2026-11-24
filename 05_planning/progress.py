from typing import Literal
from pydantic import BaseModel

class Step(BaseModel):
    goal: str
    status: Literal["pending", "running", "done", "failed", "skipped"] = "pending"
    result: str = ""
    denied: bool = False

def track(plan):
    return [Step(goal=goal) for goal in plan.steps]

import json

def step_context(task, step, history):
    return json.dumps({
        "task": task,
        "current_step": step.goal,
        "completed": [s.model_dump() for s in history
                      if s.status == "done"],
        "instruction": "Execute only the current step."
    }, ensure_ascii=False)

from stateful import run_state

def execute_step(step, model, tools, context, execute=None):
    step.status = "running"
    state = run_state(context, model, tools, execute=execute)
    ok = state.status == "completed" and not state.errors
    step.status = "done" if ok else "failed"
    step.result = state.answer if ok else str(state.errors or state.answer)
    step.denied = "Denied by user" in state.errors
    return step

from planner import make_plan

def revise(model, task, history):
    context = json.dumps({
        "task": task,
        "completed": [s.model_dump() for s in history if s.status == "done"],
        "failed": [s.model_dump() for s in history if s.status == "failed"],
        "instruction": "Plan only remaining work; avoid repeating writes."
    }, ensure_ascii=False)
    return track(make_plan(model, context))

def run_plan(task, pending, history, model, tools, execute):
    for index, step in enumerate(pending):
        context = step_context(task, step, history)
        execute_step(step, model, tools, context, execute)
        history.append(step)
        if step.status == "failed":
            for rest in pending[index + 1:]:
                rest.status = "skipped"
                rest.result = "Plan interrupted"
                history.append(rest)
            return step
    return None

def execute_plan(task, model, tools, execute=None, max_replans=1):
    if max_replans < 0:
        raise ValueError("max_replans must be nonnegative")
    pending = track(make_plan(model, task))
    history = []
    for attempt in range(max_replans + 1):
        failed = run_plan(task, pending, history, model, tools, execute)
        if failed is None or failed.denied:
            return history
        if attempt < max_replans:
            pending = revise(model, task, history)
    return history
