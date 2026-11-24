from tools import TOOLS, dispatch

result = dispatch(TOOLS, "search", '{"query":"solar"}')
print([row["id"] for row in result])
print(dispatch(TOOLS, "analyze", '{"topic":"solar"}'))
