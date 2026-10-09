import cv2
import os

name = input("Employee Name: ")

poses = [
    "Look Straight",
    "Look Left",
    "Look Right",
    "Look Up",
    "Look Down",
    "Smile",
    "Turn Left",
    "Turn Right",
    "Move Near",
    "Move Far"
]

folder = f"faces/{name}"

os.makedirs(folder, exist_ok=True)

cap = cv2.VideoCapture(0)

count = 0

while count < 10:

    ret, frame = cap.read()

    text = poses[count]

    cv2.putText(
        frame,
        text,
        (20,40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0,255,0),
        2
    )

    cv2.putText(
        frame,
        f"{count+1}/10",
        (20,80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0,255,255),
        2
    )

    cv2.imshow(
        "Employee Registration",
        frame
    )

    key = cv2.waitKey(1)

    if key == ord("c"):

        cv2.imwrite(
            f"{folder}/{count}.jpg",
            frame
        )

        count += 1

if count == 10:

    print("Registration Complete")

cap.release()
cv2.destroyAllWindows()