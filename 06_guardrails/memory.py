import sqlite3
from contextlib import closing


def init(path):
    with closing(sqlite3.connect(path)) as db, db:
        db.execute("CREATE TABLE IF NOT EXISTS notes "
                   "(id INTEGER PRIMARY KEY, note TEXT NOT NULL)")


def remember(path, note):
    with closing(sqlite3.connect(path)) as db, db:
        db.execute("INSERT INTO notes(note) VALUES (?)", (note,))


def recent(path):
    with closing(sqlite3.connect(path)) as db:
        return [row[0] for row in db.execute(
            "SELECT note FROM notes ORDER BY id DESC LIMIT 5"
        )]


import json


def with_memory(task, path):
    return json.dumps({"task": task, "untrusted_memory": recent(path)})
