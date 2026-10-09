import os
import cv2
import pickle

from insightface.app import FaceAnalysis

app = FaceAnalysis(
    name="buffalo_s"
)

app.prepare(
    ctx_id=0
)

known_faces = {}

faces_folder = "faces"

for person in os.listdir(faces_folder):

    person_folder = os.path.join(
        faces_folder,
        person
    )

    embeddings = []

    for image_name in os.listdir(person_folder):

        image_path = os.path.join(
            person_folder,
            image_name
        )

        image = cv2.imread(
            image_path
        )

        if image is None:

            print(
                image_name,
                "Image not loaded"
            )

            continue

        detected_faces = app.get(
            image
        )

        print(
            image_name,
            "Faces:",
            len(detected_faces)
        )

        if len(detected_faces) == 0:

            continue

        embedding = detected_faces[0].embedding

        embeddings.append(
            embedding
        )

    if len(embeddings):

        known_faces[person] = embeddings

        print(
            person,
            len(embeddings),
            "faces registered"
        )

with open(
    "models/known_faces.pkl",
    "wb"
) as f:

    pickle.dump(
        known_faces,
        f
    )

print("Registration Complete")