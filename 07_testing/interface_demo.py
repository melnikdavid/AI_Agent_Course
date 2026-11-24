from tools import TOOLS
from tool_interface import adapt, interface_specs, invoke_readonly

registry = adapt(TOOLS)
print([x["function"]["name"] for x in interface_specs(registry)])
print(invoke_readonly(registry, "analyze", '{"topic":"solar"}'))
