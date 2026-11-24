CORPUS = [
    ("R1", "Solar output varies with daylight and weather."),
    ("R2", "Batteries store energy for later use."),
    ("R3", "Demand response reduces peak demand."),
    ("R4", "Solar costs depend on local tariffs."),
]


def search(query):
    words = query.lower().split()
    return [
        {"id": source_id, "text": text}
        for source_id, text in CORPUS
        if any(word in text.lower() for word in words)
    ]


def analyze(topic):
    rows = search(topic)
    return {"matches": len(rows),
            "source_ids": [row["id"] for row in rows]}
