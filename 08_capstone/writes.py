from pathlib import Path
from functools import partial
from schemas import SaveArgs, RememberArgs
from memory import remember
from tools import TOOLS


def save(report):
    Path("report.md").write_text(report, encoding="utf-8")
    return "Saved report.md"


def registry(path):
    return {**TOOLS,
            "save": (SaveArgs, save, "Save report.md"),
            "remember": (RememberArgs, partial(remember, path),
                         "Store a note")}
