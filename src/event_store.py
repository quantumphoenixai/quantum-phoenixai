"""Persistent JSONL storage for Quantum Phoenix events and alerts."""

import json
from pathlib import Path
from typing import Any, Iterable

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EVENTS_FILE = PROJECT_ROOT / "data" / "events.jsonl"
ALERTS_FILE = PROJECT_ROOT / "data" / "alerts.jsonl"


def append_jsonl(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(record, sort_keys=True) + "\n")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []

    records = []
    with path.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(f"Invalid JSON in {path} at line {line_number}") from error
            if not isinstance(record, dict):
                raise ValueError(f"Expected an object in {path} at line {line_number}")
            records.append(record)
    return records


def append_event(event: dict[str, Any], path: Path = EVENTS_FILE) -> None:
    append_jsonl(path, event)


def read_events(path: Path = EVENTS_FILE) -> list[dict[str, Any]]:
    return read_jsonl(path)


def append_alert(alert: dict[str, Any], path: Path = ALERTS_FILE) -> None:
    append_jsonl(path, alert)


def read_alerts(path: Path = ALERTS_FILE) -> list[dict[str, Any]]:
    return read_jsonl(path)


def write_jsonl(path: Path, records: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as stream:
        for record in records:
            stream.write(json.dumps(record, sort_keys=True) + "\n")
