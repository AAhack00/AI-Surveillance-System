import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(0)

while True:

    success, frame = cap.read()

    results = model(frame)

    annotated = results[0].plot()

    cv2.imshow("AI Surveillance", annotated)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()