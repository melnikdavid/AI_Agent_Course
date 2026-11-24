from agent import run
from llm import chat
from memory import init, with_memory
from planner import make_plan, planned_task
from policy import approve, guarded_executor
from writes import registry
from replay import Replay, call


def research(task, model, path, approval):
    init(path)
    plan = make_plan(model, task)
    context = with_memory(planned_task(task, plan), path)
    tools = registry(path)
    execute = guarded_executor(tools, approval)
    return run(context, model, tools, execute=execute)


def demo_model():
    return Replay(
        {"role": "assistant", "content":
         '{"steps":["Search solar","Save report"]}'},
        call("search", '{"query":"solar"}', "c1"),
        call("analyze", '{"topic":"solar"}', "c2"),
        call("remember", '{"note":"Prefer concise reports"}', "c3"),
        call("save", '{"report":"Solar: R1 and R4"}', "c4"),
        {"role": "assistant", "content":
         "Demo complete. Check tool approvals and report file."},
    )


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("task", nargs="?", default="Research solar")
    args = parser.parse_args()
    model = demo_model() if args.demo else chat
    print(research(args.task, model, "memory.db", approve))


if __name__ == "__main__":
    main()
