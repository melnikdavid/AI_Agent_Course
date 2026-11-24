import json
import logging
from pydantic import ValidationError

PROTECTED = {"save", "remember"}


def approve(name, args):
    print(name, json.dumps(args, ensure_ascii=True))
    return input("Allow? [y/N] ").strip().lower() == "y"


def guarded_call(tools, approval, name, raw):
    if name not in tools:
        return {"error": "Unknown tool"}
    schema, fn, _ = tools[name]
    args = schema.model_validate_json(raw).model_dump()
    if name in PROTECTED and not approval(name, args):
        return {"error": "Denied by user"}
    return fn(**args)


def guarded_executor(tools, approval):
    seen = set()

    def execute(name, raw):
        try:
            key = (name, json.dumps(json.loads(raw), sort_keys=True))
            if key in seen:
                return {"error": "Repeated call blocked"}
            seen.add(key)
            logging.info("tool=%s", name)
            return guarded_call(tools, approval, name, raw)
        except (ValueError, ValidationError, OSError) as exc:
            return {"error": type(exc).__name__}
    return execute
