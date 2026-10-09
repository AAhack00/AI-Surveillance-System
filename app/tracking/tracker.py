import cv2
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

# Load YOLO model
model = YOLO("yolov8n.pt")

# Initialize DeepSORT tracker
tracker = DeepSort(
    max_age=100,
    n_init=5,
    max_cosine_distance=0.3
)

# Open webcam
cap = cv2.VideoCapture(0)

# Entry line position
line_y = 300

# Store counted IDs
counted_ids = set()

# Store all visitors
entered_ids = set()

while True:

    ret, frame = cap.read()

    if not ret:
        break

    results = model(frame)

    detections = []

    # Detect persons
    for result in results:

        for box in result.boxes:

            cls = int(box.cls[0])

            # Person class only
            if cls == 0:

                confidence = float(box.conf[0])

                # Ignore low confidence detections
                if confidence < 0.60:
                    continue

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )

                width = x2 - x1
                height = y2 - y1

                # Ignore very small detections
                if width < 80:
                    continue

                if height < 120:
                    continue

                detections.append(
                    (
                        [x1, y1, width, height],
                        confidence,
                        "person"
                    )
                )

    # Update tracker
    tracks = tracker.update_tracks(
        detections,
        frame=frame
    )

    person_count = 0

    for track in tracks:

        if not track.is_confirmed():
            continue

        track_id = track.track_id

        person_count += 1

        entered_ids.add(track_id)

        x1, y1, x2, y2 = map(
            int,
            track.to_ltrb()
        )

        # Center point of person
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2

        # Draw center point
        cv2.circle(
            frame,
            (center_x, center_y),
            5,
            (0, 0, 255),
            -1
        )

        # Entry detection
        if center_y > line_y:

            if track_id not in counted_ids:

                counted_ids.add(track_id)

                print(
                    f"Entry Detected: ID {track_id}"
                )

        # Draw rectangle
        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        # Draw ID
        cv2.putText(
            frame,
            f"ID {track_id}",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

    # Draw entry line
    cv2.line(
        frame,
        (0, line_y),
        (640, line_y),
        (0, 0, 255),
        3
    )

    # Display people count
    cv2.putText(
        frame,
        f"People: {person_count}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    # Display total visitors
    cv2.putText(
        frame,
        f"Visitors: {len(entered_ids)}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 0, 0),
        2
    )

    # Display entries
    cv2.putText(
        frame,
        f"Entries: {len(counted_ids)}",
        (20, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2
    )

    cv2.imshow(
        "AI Person Tracking",
        frame
    )

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()