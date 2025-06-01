from ctypes import POINTER
from ctypes import CDLL
from ctypes import RTLD_GLOBAL
from ctypes import Structure
from ctypes import c_char
from ctypes import c_double
import kdtree_wrapper
import os
import platform

class EmbeddingReg(Structure):
    _fields_ = [
        ("uid", c_char * 100),
        ("embedding", c_double * 128)
    ]

system = platform.system()
if system == "Windows":
    extension = ".dll"
if system == "Linux":
    extension = ".so"
if extension == None:
    raise RuntimeError(f"Unsupported operating system: {system}. This script only works on Windows and Linux")

CLANG_SHARED_LIBS_PATH = os.getenv("CLANG_SHARED_LIBS_PATH")
lib = CDLL(f"{CLANG_SHARED_LIBS_PATH}/lib-facial-embedding{extension}", mode=RTLD_GLOBAL)

lib.facial_embedding_get_tree.argtypes = []
lib.facial_embedding_get_tree.restype = POINTER(kdtree_wrapper.Tree)

lib.facial_embedding_build_tree.argtypes = []
lib.facial_embedding_build_tree.restype = None

lib.facial_embedding_insert_reg.argtypes = [ EmbeddingReg ]
lib.facial_embedding_insert_reg.restype = None

lib.facial_embedding_search_nearest.argtypes = [ EmbeddingReg ]
lib.facial_embedding_search_nearest.restype = EmbeddingReg
