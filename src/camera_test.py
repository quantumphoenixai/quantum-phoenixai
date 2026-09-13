import cv2

cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()

    if not success:
        print("Could not read camera")
        break

    cv2.imshow("Quantum Phoenix Camera", frame)

    if cv2.waitKey(1) == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()
