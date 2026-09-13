from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()

    if not success:
        break

    results = model(frame)

    names = results[0].names

    for box in results[0].boxes:
        cls = int(box.cls)
        conf = float(box.conf)

        if conf > 0.6:
            print(f"Detected: {names[cls]} ({conf:.2f})")

    cv2.imshow("Quantum Phoenix", results[0].plot())

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()