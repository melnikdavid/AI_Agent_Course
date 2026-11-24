from agent import run
from replay import Replay, call
from tools import TOOLS
from memory import init, remember, recent
from writes import registry
from policy import guarded_executor


def test_loop():
    model = Replay(call("search", '{"query":"solar"}'),
                   {"role": "assistant", "content": "R1/R4"})
    assert run("solar", model, TOOLS) == "R1/R4"


def test_observation():
    def model(messages, tools):
        if messages[-1]["role"] == "user":
            return call("search", '{"query":"solar"}')
        assert messages[-1]["tool_call_id"] == "c1"
        assert "R1" in messages[-1]["content"]
        assert "R4" in messages[-1]["content"]
        return {"role": "assistant", "content": "done"}
    assert run("solar", model, TOOLS) == "done"


def test_denial(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    init("notes.db")
    execute = guarded_executor(registry("notes.db"), lambda n, a: False)
    assert execute("save", '{"report":"draft"}')["error"] == "Denied by user"
    assert not (tmp_path / "report.md").exists()


def test_memory(tmp_path):
    db = tmp_path / "notes.db"
    init(db)
    remember(db, "short reports")
    assert recent(db) == ["short reports"]


def test_budget():
    model = Replay(call("search", '{"query":"solar"}'))
    assert run("solar", model, TOOLS, max_steps=1).startswith("Stopped")


def test_repeat():
    execute = guarded_executor(TOOLS, lambda n, a: False)
    raw = '{"query":"solar"}'
    assert len(execute("search", raw)) == 2
    assert execute("search", raw)["error"] == "Repeated call blocked"


def test_approved_write(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    execute = guarded_executor(registry("notes.db"), lambda n, a: True)
    assert execute("save", '{"report":"R1"}') == "Saved report.md"
    assert (tmp_path / "report.md").read_text() == "R1"


def test_invalid():
    execute = guarded_executor(TOOLS, lambda n, a: False)
    assert "error" in execute("search", '{"query":""}')
    assert execute("missing", "{}")["error"] == "Unknown tool"
