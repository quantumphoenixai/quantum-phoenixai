"""Deterministic rules for converting events into actionable alerts."""

from datetime import datetime, timezone
from typing import Any

try:
    from .event_store import append_alert
except ImportError:
    from event_store import append_alert

DEFAULT_RULES = {
    "prolonged_presence_seconds": 60.0,
    "restricted_zones": {"front_door"},
    "vehicle_labels": {"car", "truck", "bus", "motorcycle", "vehicle"},
}


def _alert(rule: str, message: str, event: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "alert": rule,
        "message": message,
        "track_id": event.get("track_id"),
        "label": event.get("label"),
        "source_event": event.get("event"),
        "zone": event.get("zone"),
    }


def evaluate_event(event: dict[str, Any], rules: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    active_rules = {**DEFAULT_RULES, **(rules or {})}
    event_type = event.get("event")
    alerts = []

    if event_type == "left" and float(event.get("duration", 0)) > active_rules["prolonged_presence_seconds"]:
        alerts.append(_alert(
            "prolonged_presence",
            f"{event.get('label', 'Object').title()} remained for {event['duration']:.1f} seconds.",
            event,
        ))

    if event_type == "zone_entered" and event.get("zone") in active_rules["restricted_zones"]:
        alerts.append(_alert(
            "restricted_zone",
            f"{event.get('label', 'Object').title()} entered restricted zone {event['zone']}.",
            event,
        ))

    if event_type == "zone_entered" and event.get("zone") == "vehicle_area" and event.get("label") in active_rules["vehicle_labels"]:
        alerts.append(_alert(
            "vehicle_arrival",
            f"{event['label'].title()} entered the vehicle area.",
            event,
        ))

    return alerts


def evaluate_events(events: list[dict[str, Any]], alert_path=None) -> list[dict[str, Any]]:
    alerts = []
    for event in events:
        event_alerts = evaluate_event(event)
        alerts.extend(event_alerts)
        for alert in event_alerts:
            if alert_path is not None:
                append_alert(alert, alert_path)
    return alerts
