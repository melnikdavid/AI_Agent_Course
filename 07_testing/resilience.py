import time
import httpx

def transient(exc):
    if isinstance(exc, httpx.TransportError):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code in {408, 429, 500, 502, 503, 504}
    return False

def with_retry(model, attempts=3, sleep=time.sleep):
    if attempts < 1:
        raise ValueError("attempts must be positive")
    def request(messages, tools=None):
        for index in range(attempts):
            try:
                return model(messages, tools)
            except (httpx.TransportError, httpx.HTTPStatusError) as exc:
                if not transient(exc) or index == attempts - 1:
                    raise
                sleep(min(2 ** index, 8))
    return request
