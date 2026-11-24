import logging

def configure_logging():
    logging.basicConfig(level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s")

def audit_model(model):
    def request(messages, tools=None):
        logging.info("model.start")
        try:
            reply = model(messages, tools)
        except Exception:
            logging.error("model.failed")
            raise
        logging.info("model.done")
        return reply
    return request

def audit_tools(execute):
    def request(name, raw):
        logging.info("tool.start name=%s", name)
        result = execute(name, raw)
        failed = isinstance(result, dict) and "error" in result
        logging.info("tool.end name=%s failed=%s", name, failed)
        return result
    return request

def audit_approval(approval):
    def decide(name, args):
        allowed = approval(name, args)
        logging.info("approval name=%s allowed=%s", name, allowed)
        return allowed
    return decide
