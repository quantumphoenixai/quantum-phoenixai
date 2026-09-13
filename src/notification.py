"""Notification delivery for rule-generated alerts."""

from typing import Any

try:
    from .event_store import ALERTS_FILE, append_alert
except ImportError:
    from event_store import ALERTS_FILE, append_alert


def notify(alert: dict[str, Any], path=ALERTS_FILE) -> None:
    append_alert(alert, path)
    print(f"ALERT: {alert['message']}")


def notify_all(alerts: list[dict[str, Any]], path=ALERTS_FILE) -> None:
    for alert in alerts:
        notify(alert, path)
