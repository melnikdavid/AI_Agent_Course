# AI Research Agent — progressive workshop

Python 3.10+ recommended. Open one checkpoint folder at a time, or build a separate working folder by following slide instructions. Each folder includes the cumulative source at the end of that stage. Never concatenate entire checkpoint folders.

## Setup (from 01_llm)
`python -m venv .venv` (activate in your shell)
`python -m pip install -r requirements.txt`

## Offline checkpoints
Run `python demo.py` in folders 01–06. In 02 also run `python history_demo.py` and `python schema_demo.py`. In 07 run `python -m pytest -q`. In 08 run `python main.py --demo` and approve or deny the two writes. Demo responses are scripted, not AI inference. Each run uses local SQLite / report files in the working directory.

## Live provider
Copy `.env.example` to `.env` in your working folder and configure a compatible Chat Completions endpoint, model and API key. Never commit `.env`. Run `python live.py` in 01 or 03; in 08 run `python main.py "Research solar and save a report"`. The selected model must support native tool calls and follow the JSON planning prompt. Live API behavior has not been tested. Model outputs can fail validation; this is a teaching prototype, not a production service.

## Slide instructions
CREATE = new file; APPEND = paste at end with two blank lines; REPLACE = replace entire file. Each code block is complete. A stage checkpoint is runnable after the preceding operations. Source IDs R1–R4 refer to synthetic local teaching material, not published research.


## Advanced extensions (new slides)
The original workshop code remains intact. The new files are incremental additions, not replacements of the earlier labs. Use the updated bundle rather than an older GitHub checkout unless the instructor has synced the repository.

- 03_loop: `python state_demo.py` — explicit AgentState and stateful loop.
- 05_planning: `python progress_demo.py` — progress tracking and bounded replanning.
- 06_guardrails: `python retry_demo.py` — deterministic exponential backoff. Shared request/tool/time/token budget and auditing are integrated in the capstone.
- 07_testing: `python interface_demo.py` and `python -m pytest -q` — Tool Protocol adapter and extended tests.
- 08_capstone: `python advanced_demo.py` — complete offline upgraded agent; answer y to approve writing the report. Answer n to verify a denied write ends the plan. Use a clean working directory to distinguish new output from files left by previous runs.
- 08_capstone live: `python advanced_live.py "Research solar and save a report"` — set a compatible .env and choose a tool-calling model. Live behavior has not been verified against an external model provider.

The time budget is checked at action boundaries, not a hard cancellation deadline. Provider token usage is measured after successful HTTP responses when available; it may overshoot on the last request, and failed requests may have unreported usage. The code does not implement exact monetary billing or a production-grade token preflight estimator. Progress completion is a software status based on the model reply and tool error observations, not proof of factual correctness. The repeated-call policy is intentionally conservative and scoped to a single research run.
