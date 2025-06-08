from random import random
from facial_embedding_wrapper import lib as fe_lib
from facial_embedding_wrapper import EmbeddingReg

def main():
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
