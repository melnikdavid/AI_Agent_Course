class Replay:
    def __init__(self, *replies):
        self.replies = iter(replies)

    def __call__(self, messages, tools=None):
        return next(self.replies)


def call(name, arguments, call_id="c1"):
    return {"role": "assistant", "content": None,
            "tool_calls": [{"id": call_id, "type": "function",
                            "function": {"name": name,
                                         "arguments": arguments}}]}
