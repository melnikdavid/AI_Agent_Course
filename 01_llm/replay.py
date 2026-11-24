class Replay:
    def __init__(self, *replies):
        self.replies = iter(replies)

    def __call__(self, messages, tools=None):
        return next(self.replies)
