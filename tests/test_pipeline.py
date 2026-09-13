import json
import tempfile
import unittest
from pathlib import Path

from src.event_store import read_events, write_jsonl
from src.rules_engine import evaluate_event, evaluate_events
from src.summary_engine import build_summary, render_summary


class PipelineTests(unittest.TestCase):
    def test_summary_uses_labels_and_zone_activity(self):
        events = [
            {"event": "entered", "track_id": 1, "label": "person", "timestamp": "t1"},
            {"event": "zone_entered", "track_id": 1, "label": "person", "zone": "driveway", "timestamp": "t2"},
            {"event": "left", "track_id": 1, "label": "person", "duration": 74, "timestamp": "t3"},
            {"event": "entered", "track_id": 2, "label": "chair", "timestamp": "t4"},
        ]

        summary = build_summary(events)
        report = render_summary(summary)

        self.assertEqual(summary["total_tracked_objects"], 2)
        self.assertEqual(summary["zone_entries"], {"driveway": 1})
        self.assertEqual(summary["active_objects"][0]["label"], "chair")
        self.assertIn("Person #1", report)
        self.assertIn("Driveway: 1 entries", report)

    def test_rules_flag_long_stays_and_restricted_zones(self):
        long_stay = {"event": "left", "track_id": 1, "label": "person", "duration": 61}
        restricted = {"event": "zone_entered", "track_id": 2, "label": "person", "zone": "front_door"}

        self.assertEqual(evaluate_event(long_stay)[0]["alert"], "prolonged_presence")
        self.assertEqual(evaluate_event(restricted)[0]["alert"], "restricted_zone")

    def test_event_store_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.jsonl"
            records = [{"event": "entered", "track_id": 4, "label": "person"}]
            write_jsonl(path, records)
            self.assertEqual(read_events(path), records)

    def test_alerts_can_be_persisted(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "alerts.jsonl"
            events = [{"event": "left", "track_id": 1, "label": "person", "duration": 80}]
            alerts = evaluate_events(events, path)
            self.assertEqual(len(alerts), 1)
            self.assertEqual(json.loads(path.read_text())["alert"], "prolonged_presence")


if __name__ == "__main__":
    unittest.main()
