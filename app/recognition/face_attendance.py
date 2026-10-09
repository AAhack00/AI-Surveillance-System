import cv2
import pickle
import json
import time
import os

from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity
from insightface.app import FaceAnalysis

from app.attendance.attendance_manager import (
    process_attendance
)

from app.alerts.alert_manager import (
    save_alert
)

# ----------------------------------
# SECURITY SETTINGS
# ----------------------------------

with open(
    "config/security.json",
    "r"
) as f:

    security = json.load(f)

# ----------------------------------
# FACE MODEL
# ----------------------------------

app = FaceAnalysis(
    name="buffalo_s"
)

app.prepare(
    ctx_id=0
)

# ----------------------------------
# KNOWN FACES
# ----------------------------------

with open(
    "models/known_faces.pkl",
    "rb"
) as f:

    known_faces = pickle.load(f)

# ----------------------------------
# CAMERA
# ----------------------------------

cap = cv2.VideoCapture(
    0,
    cv2.CAP_DSHOW
)

cap.set(
    cv2.CAP_PROP_FRAME_WIDTH,
    640
)

cap.set(
    cv2.CAP_PROP_FRAME_HEIGHT,
    480
)

recognized_people = set()
last_detection = {}

last_unknown_save = 0

frame_count = 0

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame_count += 1

    if frame_count % 3 != 0:
        continue

    unknown_count = 0

    faces = app.get(frame)

    for face in faces:

        embedding = face.embedding

        best_score = 0

        best_name = "Unknown"

        name = "Unknown"

        for person, embeddings in known_faces.items():

            for emb in embeddings:

                score = cosine_similarity(
                    embedding.reshape(1, -1),
                    emb.reshape(1, -1)
                )[0][0]

                if score > best_score:

                    best_score = score

                    best_name = person

        print(
            f"Best Match: {best_name} | Score: {best_score:.3f}"
        )

        current_time = time.time()

        if best_score > 0.35:

            name = best_name

            recognized_people.add(name)

            if name not in last_detection:

                status = process_attendance(
                    name
                )

                last_detection[name] = current_time

                print(
                    name,
                    status
                )

            elif current_time - last_detection[name] > 30:

                status = process_attendance(
                    name
                )

                last_detection[name] = current_time

                print(
                    name,
                    status
                )

            color = (0,255,0)

        else:

            name = "Unknown"

            color = (0,165,255)

            unknown_count += 1

            save_alert(
                "Unknown Person"
            )

            if current_time - last_unknown_save >= 60:

                last_unknown_save = current_time

                timestamp = datetime.now().strftime(
                    "%d-%B-%Y___%I-%M-%S_%p"
                )

                filename = (
                    "evidence/images/"
                    f"{name}_{timestamp}.jpg"
                )

                cv2.imwrite(
                    filename,
                    frame
                )

        box = face.bbox.astype(int)

        x1, y1, x2, y2 = box

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            color,
            2
        )

        cv2.putText(
            frame,
            f"{name} ({best_score:.2f})",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            color,
            2
        )

    status = {

        "people": len(faces),

        "recognized": list(
            recognized_people
        ),

        "unknown": unknown_count,

        "alerts": unknown_count
    }

    os.makedirs(
        "data",
        exist_ok=True
    )

    with open(
        "data/system_status.json",
        "w"
    ) as file:

        json.dump(
            status,
            file
        )

    cv2.imwrite(
        "data/live_frame.jpg",
        frame
    )

    cv2.imshow(
        "AI Surveillance System",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()

cv2.destroyAllWindows()