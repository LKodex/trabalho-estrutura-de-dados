from dotenv import load_dotenv
load_dotenv()

from facial_embedding_wrapper import lib as fe_lib
from facial_embedding_wrapper import EmbeddingReg
from kdtree_wrapper import lib as kdt_lib
from kdtree_wrapper import Node as KDTreeNode
from kdtree_wrapper import Tree as KDTree
from fastapi import FastAPI
from pydantic import BaseModel
from hashlib import sha3_384
from ctypes import c_double
from time import time

Embeddings = list[float]

class PictureEmbeddings(BaseModel):
    uid: str
    embedding: Embeddings

app = FastAPI()

@app.get("/")
async def root():
    return { "message": "Hello, world!" }

fe_lib.facial_embedding_build_tree()
@app.post("/build-tree")
async def build_tree():
    return {
        "message": "Tree pre-built to avoid error prone behavior"
    }

@app.post("/insert")
async def insert(picture_embeddings: PictureEmbeddings):
    byte_hash = picture_embeddings.uid[:99].encode("utf-8")
    reg = EmbeddingReg(
        uid=byte_hash,
        embedding=(c_double * 128)(*picture_embeddings.embedding)
    )
    fe_lib.facial_embedding_insert_reg(reg)
    return {
        "message": f"Picture {picture_embeddings.uid} insert successfully"
    }

@app.post("/search")
async def search(embeddings: Embeddings):
    query = EmbeddingReg(
        uid=str(time()).encode("utf-8"),
        embedding=(c_double * 128)(*embeddings)
    )
    res: bytes = fe_lib.facial_embedding_search_nearest(query)
    return {
        "uid": res.uid.decode("utf-8"),
        "embedding": list(res.embedding)
    }

def main():
    from random import random
    from facial_embedding_wrapper import lib as fe_lib
    from facial_embedding_wrapper import EmbeddingReg

    fe_lib.facial_embedding_build_tree()

    for i in range(1000):
        reg = EmbeddingReg()
        reg.uid = str(i).encode("utf-8")
        for j in range(128):
            reg.embedding[j] = random()
        fe_lib.facial_embedding_insert_reg(reg)

    sreg = EmbeddingReg()
    sreg.uid = "search".encode("utf-8")
    for i in range(128):
        sreg.embedding[i] = random()
    rreg = fe_lib.facial_embedding_search_nearest(sreg)
    print(rreg)

    for i in range(128):
        print(f"[{i:3}] {sreg.uid.decode("utf-8")}:\t{sreg.embedding[i]}")
        print(f"[{i:3}] {rreg.uid.decode("utf-8")}:\t{rreg.embedding[i]}")

if __name__ == "__main__":
    main()
