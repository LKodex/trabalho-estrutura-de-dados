from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return { "message": "Hello, world!" }

def main():
    from random import random
    from facial_embedding_wrapper import lib as few_lib
    from facial_embedding_wrapper import EmbeddingReg

    few_lib.facial_embedding_build_tree()

    for i in range(1000):
        reg = EmbeddingReg()
        reg.uid = str(i).encode("utf-8")
        for j in range(128):
            reg.embedding[j] = random()
        few_lib.facial_embedding_insert_reg(reg)

    sreg = EmbeddingReg()
    sreg.uid = "search".encode("utf-8")
    for i in range(128):
        sreg.embedding[i] = random()
    rreg = few_lib.facial_embedding_search_nearest(sreg)
    print(rreg)

    for i in range(128):
        print(f"[{i:3}] {sreg.uid.decode("utf-8")}:\t{sreg.embedding[i]}")
        print(f"[{i:3}] {rreg.uid.decode("utf-8")}:\t{rreg.embedding[i]}")

if __name__ == "__main__":
    main()
