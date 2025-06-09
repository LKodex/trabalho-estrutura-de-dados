from deepface import DeepFace
import sys
import os
import json

file = sys.argv[1]

embeddings = DeepFace.represent(file, model_name="Facenet")

data = {
    "uid": os.path.basename(file),
    "embeddings": embeddings[0]["embedding"]
}

print(json.dumps(data))
