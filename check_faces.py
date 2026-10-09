# check_faces.py

import pickle

with open(
    "models/known_faces.pkl",
    "rb"
) as f:

    data = pickle.load(f)

print(data.keys())

for person in data:

    print(
        person,
        len(data[person])
    )