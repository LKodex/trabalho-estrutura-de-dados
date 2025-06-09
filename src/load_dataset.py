from dotenv import load_dotenv
load_dotenv()

import os
from deepface import DeepFace
import random
import requests
import sys

def list_jpg_files(path):
    path = os.path.abspath(path)
    files = [ os.path.join(dirpath, f) for (dirpath, _dirnames, filenames) in os.walk(path) for f in filenames if f.endswith(".jpg") ]
    return files

faces_error = 0
success_count = 0

def main():
    path = os.getenv("FACE_PICTURES_FOLDER")
    files = list_jpg_files(path)
    selected_files = random.sample(files, 1000)
    for file in selected_files:
        try:
            embeddings = DeepFace.represent(file, model_name="Facenet")
            post_embedding(os.path.basename(file), embeddings[0]["embedding"])
        except ValueError as e:
            global faces_error
            faces_error += 1
            print(f"[ERR] ({faces_error}) {e}", file=sys.stderr)

error_counter = 0

def post_embedding(name: str, embeddings: list[float]):
    data = {
        "uid": name,
        "embedding": embeddings
    }
    host = os.getenv("API_HOST")
    endpoint = os.getenv("API_INSERT_ENDPOINT")
    url = f"{host}{endpoint}"
    response = requests.post(url, json=data)
    HTTP_OK = 200
    HTTP_CREATED = 201
    if response.status_code not in [ HTTP_OK, HTTP_CREATED ]:
        global error_counter
        error_counter += 1
        print(f"[ERR] ({error_counter}) Failed to POST {name}. HTTP Status: {response.status_code}", file=sys.stderr)
    else:
        global success_count
        success_count += 1
        print(f"[LOG] ({success_count}) Successfully sent picture {name}", file=sys.stdout)
        
if __name__ == "__main__":
    main()
