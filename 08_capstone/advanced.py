from budget import Budget, BudgetExceeded, budget_model, budget_tools
from resilience import with_retry
from audit import audit_model, audit_tools, audit_approval
from provider_usage import provider_model
from policy import guarded_executor
from tool_interface import adapt, bridge

def build_runtime(model, tools, approval, budget):
    if model is None:
        model = provider_model(budget)
    model = with_retry(budget_model(audit_model(model), budget))
    tools = bridge(adapt(tools))
    execute = guarded_executor(tools, audit_approval(approval))
    execute = budget_tools(audit_tools(execute), budget)
    return model, tools, execute

import logging
from audit import configure_logging
from memory import init, with_memory
from writes import registry
from progress import execute_plan

def advanced_research(task, model, path, approval, budget=None):
    configure_logging()
    logging.info("task.start")
    budget = budget or Budget()
    init(path)
    model, tools, execute = build_runtime(model, registry(path), approval, budget)
    try:
        steps = execute_plan(with_memory(task, path), model, tools, execute)
    except Exception as exc:
        logging.error("task.failed type=%s", type(exc).__name__)
        raise
    logging.info("task.end steps=%s", len(steps))
    return steps
