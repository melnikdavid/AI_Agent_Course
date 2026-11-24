from state import AgentState
from tool_interface import adapt, invoke_readonly
from tools import TOOLS

def test_state_isolation():
    a, b = AgentState("a"), AgentState("b")
    a.errors.append("x")
    assert not b.errors

def test_interface():
    assert invoke_readonly(adapt(TOOLS), "save", "{}") == {
        "error": "Not an approved read-only tool"}
    assert invoke_readonly(adapt(TOOLS), "analyze",
                           '{"topic":"solar"}')["matches"] == 2

import pytest
import httpx
from budget import Budget, BudgetExceeded, budget_model, record_usage
from resilience import with_retry

def test_budget_counts_retries():
    def fail(messages, tools=None):
        raise httpx.ConnectError("offline")
    b = Budget(max_requests=2)
    with pytest.raises(BudgetExceeded):
        with_retry(budget_model(fail, b), sleep=lambda _: None)([])
    assert b.requests == 2

def test_usage_limit():
    b = Budget(max_tokens=10)
    record_usage(b, None)
    with pytest.raises(BudgetExceeded):
        record_usage(b, {"total_tokens": 10})
    assert (b.tokens, b.unknown_usage) == (10, 1)

from progress import execute_plan
from replay import Replay, call

def reply(text):
    return {"role": "assistant", "content": text}

def test_replan():
    model = Replay(reply('{"steps":["First","Later"]}'),
        call("missing", "{}"), reply("Failed"),
        reply('{"steps":["Fallback"]}'), reply("Recovered"))
    steps = execute_plan("Research solar", model, TOOLS)
    assert [s.status for s in steps] == ["failed", "skipped", "done"]

def test_denial_stops_plan():
    model = Replay(reply('{"steps":["Save","Continue"]}'),
                   call("save", "{}"), reply("Denied"))
    execute = lambda name, raw: {"error": "Denied by user"}
    steps = execute_plan("Research solar", model, TOOLS, execute)
    assert [s.status for s in steps] == ["failed", "skipped"]

def test_no_retry_on_401():
    waits = []
    def unauthorized(messages, tools=None):
        response = httpx.Response(401, request=httpx.Request("POST", "https://example.com"))
        response.raise_for_status()
    with pytest.raises(httpx.HTTPStatusError):
        with_retry(unauthorized, sleep=waits.append)([])
    assert waits == []
