"""Command-line report and alert generation."""

import argparse

from event_store import ALERTS_FILE, read_events
from notification import notify_all
from rules_engine import evaluate_events
from summary_engine import build_summary, render_summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a Quantum Phoenix report")
    parser.add_argument(
        "--alerts",
        action="store_true",
        help="evaluate rules and write notifications to data/alerts.jsonl",
    )
    args = parser.parse_args()

    events = read_events()
    summary = build_summary(events)
    print(render_summary(summary))

    if args.alerts:
        alerts = evaluate_events(events)
        notify_all(alerts)
        print(f"\nAlerts generated: {len(alerts)}")
        print(f"Alert history: {ALERTS_FILE}")


if __name__ == "__main__":
    main()
