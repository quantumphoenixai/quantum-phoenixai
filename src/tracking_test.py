from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()

    if not success:
        break

    results = model.track(frame, persist=True, verbose=False)

    if results[0].boxes is not None:
        for box in results[0].boxes:
            cls = int(box.cls)
            conf = float(box.conf)

            if conf > 0.7:
                label = results[0].names[cls]
                print(f"There is a {label} ({conf:.2f})")

    annotated = results[0].plot()

    cv2.imshow("Quantum Phoenix", annotated)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()