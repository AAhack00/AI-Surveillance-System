import cv2
from insightface.app import FaceAnalysis

app = FaceAnalysis()

app.prepare(ctx_id=0)

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    faces = app.get(frame)

    for face in faces:

        box = face.bbox.astype(int)

        x1, y1, x2, y2 = box

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0,255,0),
            2
        )

        cv2.putText(
            frame,
            "Face",
            (x1, y1-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0,255,0),
            2
        )

    cv2.imshow(
        "Face Detection",
        frame
    )

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()