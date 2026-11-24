import argparse
from advanced import advanced_research, BudgetExceeded
from budget import Budget
from policy import approve

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("task")
    args = parser.parse_args()
    budget = Budget()
    try:
        steps = advanced_research(args.task, None, "memory.db", approve, budget)
        for step in steps:
            print(step.status, step.goal, step.result)
    except BudgetExceeded as exc:
        print("Stopped:", exc)
    print("Usage:", budget.requests, budget.tools, budget.tokens,
          "unknown usage:", budget.unknown_usage)

if __name__ == "__main__":
    main()
