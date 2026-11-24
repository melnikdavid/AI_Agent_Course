from schemas import SearchArgs, AnalyzeArgs
from research import search, analyze

TOOLS = {
    "search": (SearchArgs, search, "Search local sources"),
    "analyze": (AnalyzeArgs, analyze, "Count matching sources"),
}


def specs(tools):
    return [
        {"type": "function", "function": {
            "name": name, "description": desc,
            "parameters": schema.model_json_schema(),
        }}
        for name, (schema, fn, desc) in tools.items()
    ]


def dispatch(tools, name, raw):
    if name not in tools:
        return {"error": "Unknown tool"}
    schema, fn, _ = tools[name]
    args = schema.model_validate_json(raw)
    return fn(**args.model_dump())
