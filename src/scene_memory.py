from ultralytics import YOLO
import cv2
import time
import json
from datetime import datetime

from event_store import append_event
from notification import notify
from rules_engine import evaluate_event

ZONES = {
    "front_door": (0.05, 0.20, 0.30, 0.80),
    "driveway": (0.32, 0.45, 0.68, 0.95),
    "vehicle_area": (0.70, 0.30, 0.95, 0.80),
}


def log_event(event_data):
    append_event(event_data)
    for alert in evaluate_event(event_data):
        notify(alert)


def zones_for_point(x, y, frame_width, frame_height):
    normalized_x = x / frame_width
    normalized_y = y / frame_height

    return {
        zone_name
        for zone_name, (left, top, right, bottom) in ZONES.items()
        if left <= normalized_x <= right and top <= normalized_y <= bottom
    }


model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(0)

# Memory storage
scene_memory = {}

while True:
    success, frame = cap.read()

    if not success:
        break

    results = model.track(frame, persist=True, verbose=False)

    current_ids = set()

    if results[0].boxes is not None and results[0].boxes.id is not None:

        boxes = results[0].boxes

        for i in range(len(boxes)):

            track_id = int(boxes.id[i])
            class_id = int(boxes.cls[i])

            label = results[0].names[class_id]
            left, top, right, bottom = boxes.xyxy[i].tolist()
            center_x = (left + right) / 2
            center_y = (top + bottom) / 2
            current_zones = zones_for_point(
                center_x,
                center_y,
                frame.shape[1],
                frame.shape[0],
            )

            current_ids.add(track_id)

            # New object
            if track_id not in scene_memory:

                scene_memory[track_id] = {
                    "label": label,
                    "first_seen": time.time(),
                    "last_seen": time.time(),
                    "zones": set()
                }

                event = {
                    "timestamp": datetime.now().isoformat(),
                    "event": "entered",
                    "track_id": track_id,
                    "label": label
                }
                print(f"EVENT: {label} #{track_id} entered scene")
                log_event(event)

            # Existing object
            else:
                scene_memory[track_id]["last_seen"] = time.time()

            previous_zones = scene_memory[track_id]["zones"]
            entered_zones = current_zones - previous_zones

            for zone_name in sorted(entered_zones):
                zone_event = {
                    "timestamp": datetime.now().isoformat(),
                    "event": "zone_entered",
                    "zone": zone_name,
                    "label": label,
                    "track_id": track_id,
                }
                print(
                    f"EVENT: {label} #{track_id} entered {zone_name} zone"
                )
                log_event(zone_event)

            scene_memory[track_id]["zones"] = current_zones

        # Check for disappeared objects
        tracked_ids = list(scene_memory.keys())

        for old_id in tracked_ids:

            if old_id not in current_ids:

                first_seen = scene_memory[old_id]["first_seen"]
                last_seen = scene_memory[old_id]["last_seen"]

                duration = last_seen - first_seen

                label = scene_memory[old_id]["label"]

                event = {
                    "timestamp": datetime.now().isoformat(),
                    "event": "left",
                    "label": label,
                    "track_id": old_id,
                    "duration": round(duration, 1)
                }

                print(
                    f"EVENT: {label} #{old_id} left scene "
                    f"after {duration:.1f} seconds"
                )

                log_event(event)

                del scene_memory[old_id]

    annotated = results[0].plot()

    for zone_name, (left, top, right, bottom) in ZONES.items():
        x1 = int(left * frame.shape[1])
        y1 = int(top * frame.shape[0])
        x2 = int(right * frame.shape[1])
        y2 = int(bottom * frame.shape[0])
        cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 200, 255), 2)
        cv2.putText(
            annotated,
            zone_name.replace("_", " "),
            (x1 + 5, y1 + 22),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 200, 255),
            2,
        )

    cv2.imshow("Quantum Phoenix Scene Memory", annotated)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
