from ctypes import POINTER
from ctypes import CDLL
from ctypes import Structure
from ctypes import c_char
from ctypes import c_double
from . import kdtree_wrapper

class EmbeddingReg(Structure):
    _fields_ = [
        ("uid", c_char * 100),
        ("embedding", c_double * 128)
    ]

lib = CDLL("./lib/lib-facial-embedding.so")

lib.facial_embedding_get_tree.argtypes = []
lib.facial_embedding_get_tree.restype = POINTER(kdtree_wrapper.Tree)

lib.facial_embedding_build_tree.argtypes = []
lib.facial_embedding_build_tree.restype = None

lib.facial_embedding_insert_reg.argtypes = [ EmbeddingReg ]
lib.facial_embedding_insert_reg.restype = None

lib.facial_embedding_search_nearest.argtypes = [ EmbeddingReg ]
lib.facial_embedding_search_nearest.restype = EmbeddingReg
