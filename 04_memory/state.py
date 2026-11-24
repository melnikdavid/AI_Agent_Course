from dataclasses import dataclass, field

@dataclass
class AgentState:
    task: str
    messages: list[dict] = field(default_factory=list)
    turns: int = 0
    tool_calls: int = 0
    status: str = "running"
    answer: str = ""
    errors: list[str] = field(default_factory=list)
