def ask(model, history, text):
    history.append({"role": "user", "content": text})
    reply = model(history)
    history.append(reply)
    return reply["content"]
