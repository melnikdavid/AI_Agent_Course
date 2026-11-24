import json
from agent import initial_messages, observe
from tools import specs, dispatch
from state import AgentState

def start(task):
    return AgentState(task, initial_messages(task))

def stop(state, status, answer):
    state.status = status
    state.answer = answer
    return state

def turn(state, model, tools, execute, limit):
    reply = model(state.messages, specs(tools))
    state.turns += 1
    state.messages.append(reply)
    calls = reply.get("tool_calls") or []
    if not calls:
        answer = reply.get("content") or ""
        return stop(state, "completed" if answer else "failed", answer)
    for request in calls:
        if state.tool_calls >= limit:
            return stop(state, "stopped", "Tool budget exhausted")
        state.tool_calls += 1
        result = observe(request, execute)
        state.messages.append(result)
        data = json.loads(result["content"])
        if isinstance(data, dict) and "error" in data:
            state.errors.append(str(data["error"]))
    return state

def run_state(task, model, tools, max_steps=8,
              execute=None, max_tools=20):
    state = start(task)
    execute = execute or (lambda n, a: dispatch(tools, n, a))
    for _ in range(max_steps):
        turn(state, model, tools, execute, max_tools)
        if state.status != "running":
            return state
    return stop(state, "stopped", "Step budget exhausted")
