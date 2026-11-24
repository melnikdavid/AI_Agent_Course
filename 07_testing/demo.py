from pathlib import Path
from memory import init
from writes import registry
from policy import guarded_executor

init("memory.db")
tools = registry("memory.db")
execute = guarded_executor(tools, lambda name, args: False)
before = Path("report.md").exists()
print(execute("save", '{"report":"Draft"}'))
print(Path("report.md").exists() == before)
