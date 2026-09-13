from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(0)

known_ids = set()

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

            cls = int(boxes.cls[i])

            label = results[0].names[cls]

            current_ids.add(track_id)

            if track_id not in known_ids:
                print(f"EVENT: {label} #{track_id} entered scene")

        for old_id in known_ids:
            if old_id not in current_ids:
                print(f"EVENT: object #{old_id} left scene")

        known_ids = current_ids.copy()

    annotated = results[0].plot()

    cv2.imshow("Quantum Phoenix Event Tracker", annotated)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()