from typing import Protocol
from pydantic import BaseModel

class Tool(Protocol):
    description: str
    schema: type[BaseModel]
    def invoke(self, raw: str) -> object: ...

from dataclasses import dataclass
from typing import Callable

@dataclass
class FunctionTool:
    schema: type[BaseModel]
    fn: Callable
    description: str

    def invoke(self, raw: str) -> object:
        args = self.schema.model_validate_json(raw)
        return self.fn(**args.model_dump())

def adapt(registry) -> dict[str, Tool]:
    return {name: FunctionTool(*entry) for name, entry in registry.items()}

def interface_specs(tools: dict[str, Tool]):
    return [{"type": "function", "function": {
        "name": name, "description": tool.description,
        "parameters": tool.schema.model_json_schema(),
    }} for name, tool in tools.items()]

def invoke_readonly(tools: dict[str, Tool], name, raw):
    if name not in {"search", "analyze"} or name not in tools:
        return {"error": "Not an approved read-only tool"}
    return tools[name].invoke(raw)

import json

def bridge(tools: dict[str, Tool]):
    def validated_call(tool):
        def call(**args):
            return tool.invoke(json.dumps(args))
        return call
    return {name: (tool.schema, validated_call(tool), tool.description)
            for name, tool in tools.items()}
