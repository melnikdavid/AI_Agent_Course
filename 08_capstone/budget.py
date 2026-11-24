from dataclasses import dataclass, field
from time import monotonic

class BudgetExceeded(RuntimeError):
    pass

@dataclass
class Budget:
    max_requests: int = 30
    max_tools: int = 20
    max_tokens: int = 30000
    seconds: float = 120
    requests: int = 0
    tools: int = 0
    tokens: int = 0
    unknown_usage: int = 0
    started: float = field(default_factory=monotonic)

def check_time(budget):
    if monotonic() - budget.started >= budget.seconds:
        raise BudgetExceeded("time budget")

def take_request(budget):
    check_time(budget)
    if budget.requests >= budget.max_requests:
        raise BudgetExceeded("request budget")
    if budget.tokens >= budget.max_tokens:
        raise BudgetExceeded("token budget")
    budget.requests += 1

def take_tool(budget):
    check_time(budget)
    if budget.tools >= budget.max_tools:
        raise BudgetExceeded("tool budget")
    budget.tools += 1

def budget_model(model, budget):
    def request(messages, tools=None):
        take_request(budget)
        reply = model(messages, tools)
        check_time(budget)
        return reply
    return request

def budget_tools(execute, budget):
    def request(name, raw):
        take_tool(budget)
        result = execute(name, raw)
        check_time(budget)
        return result
    return request

def record_usage(budget, usage):
    total = usage.get("total_tokens") if isinstance(usage, dict) else None
    if not isinstance(total, int) or total < 0:
        budget.unknown_usage += 1
        return
    budget.tokens += total
    if budget.tokens >= budget.max_tokens:
        raise BudgetExceeded("token budget")
