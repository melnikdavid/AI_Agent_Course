from schemas import Plan


def make_plan(model, task):
    messages = [
        {"role": "system", "content":
         'Return only JSON: {"steps":["step"]}. Max 5 steps.'},
        {"role": "user", "content": task},
    ]
    return Plan.model_validate_json(model(messages)["content"])


import json


def planned_task(task, plan):
    return json.dumps({"task": task, "suggested_plan": plan.steps})
