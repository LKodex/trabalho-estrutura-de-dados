from ctypes import CFUNCTYPE
from ctypes import POINTER
from ctypes import CDLL
from ctypes import Structure
from ctypes import c_double
from ctypes import c_int
from ctypes import c_void_p

class Node(Structure):
    pass

Node._fields_ = [
    ("key", c_void_p),
    ("left", POINTER(Node)),
    ("right", POINTER(Node))
]

_c_cmp_func = CFUNCTYPE(c_int, c_void_p, c_void_p, c_int)
_c_dist_func = CFUNCTYPE(c_double, c_void_p, c_void_p)

class Tree(Structure):
    _fields_ = [
        ("root", POINTER(Node)),
        ("cmp", _c_cmp_func),
        ("dist", _c_dist_func),
        ("k", c_int)
    ]

# Carregar a biblioteca C
lib = CDLL("./lib/lib-kdtree.so")

# Definir a assinatura da função
lib.kdtree_build.argtypes = [ POINTER(Tree), _c_cmp_func, _c_dist_func, c_int ]
lib.kdtree_build.restype = None

lib.kdtree_insert.argtypes = [ POINTER(Tree), c_void_p ]
lib.kdtree_insert.restype = None

lib.kdtree_destroy.argtypes = [ POINTER(Tree) ]
lib.kdtree_destroy.restype = None

lib.kdtree_search_nearest.argtypes = [ POINTER(Tree), c_void_p ]
lib.kdtree_search_nearest.restype = POINTER(Node)
