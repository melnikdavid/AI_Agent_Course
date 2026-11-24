import httpx
from resilience import with_retry

calls = []
def flaky(messages, tools=None):
    calls.append(1)
    if len(calls) < 3:
        raise httpx.ConnectError("temporary")
    return {"content": "OK"}

waits = []
print(with_retry(flaky, sleep=waits.append)([]))
print(len(calls), waits)
