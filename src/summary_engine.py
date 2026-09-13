"""Turn persisted event records into human-readable situational summaries."""

from collections import Counter, defaultdict
from typing import Any


def build_summary(events: list[dict[str, Any]]) -> dict[str, Any]:
    objects: dict[int, dict[str, Any]] = {}
    zone_entries = Counter()
    event_counts = Counter()
    durations: list[float] = []

    for event in events:
        event_type = event.get("event")
        event_counts[event_type] += 1
        track_id = event.get("track_id")

        if event_type == "zone_entered":
            zone_entries[event.get("zone", "unknown")] += 1
            continue
        if track_id is None:
            continue

        record = objects.setdefault(track_id, {})
        record["label"] = event.get("label", record.get("label", "object"))
        if event_type == "entered":
            record["entered"] = event.get("timestamp")
            record.pop("left", None)
            record.pop("duration", None)
        elif event_type == "left":
            record["left"] = event.get("timestamp")
            record["duration"] = float(event.get("duration", 0))
            durations.append(record["duration"])

    label_counts = Counter(record["label"] for record in objects.values())
    active_objects = [
        {"track_id": track_id, **record}
        for track_id, record in objects.items()
        if "left" not in record
    ]

    return {
        "total_tracked_objects": len(objects),
        "event_counts": dict(event_counts),
        "label_counts": dict(label_counts),
        "zone_entries": dict(zone_entries),
        "objects": [{"track_id": track_id, **record} for track_id, record in objects.items()],
        "active_objects": active_objects,
        "completed_durations": durations,
        "average_duration": sum(durations) / len(durations) if durations else 0.0,
        "longest_duration": max(durations) if durations else 0.0,
    }


def render_summary(summary: dict[str, Any]) -> str:
    lines = ["", "=" * 40, "QUANTUM PHOENIX REPORT", "=" * 40]
    lines.append(f"\nTotal tracked objects: {summary['total_tracked_objects']}")

    for record in summary["objects"]:
        lines.append(f"\n{record['label'].title()} #{record['track_id']}")
        if record.get("entered"):
            lines.append(f"  Entered: {record['entered']}")
        if record.get("left"):
            lines.append(f"  Left: {record['left']}")
        if "duration" in record:
            lines.append(f"  Duration: {record['duration']:.1f} seconds")
        else:
            lines.append("  Status: Still present")

    if summary["zone_entries"]:
        lines.extend(["\nZone activity"])
        for zone, count in sorted(summary["zone_entries"].items()):
            lines.append(f"  {zone.replace('_', ' ').title()}: {count} entries")

    if summary["completed_durations"]:
        lines.extend([
            "\nStatistics",
            f"  Average Duration: {summary['average_duration']:.1f} seconds",
            f"  Longest Stay: {summary['longest_duration']:.1f} seconds",
        ])

    lines.extend(["\nAssessment", "  Review the alerts report for flagged activity.", "", "=" * 40])
    return "\n".join(lines)
