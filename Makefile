# Generated using AI
# Detect OS and set shared library extension
ifeq ($(OS),Windows_NT)
    EXT = dll
    SHARED_FLAG = -shared
    RM = del /Q
    MKDIR = if not exist $(subst /,\\,$(1)) mkdir $(subst /,\\,$(1))
    LIB_PREFIX = lib-
else
    UNAME_S := $(shell uname -s)
    EXT = so
    SHARED_FLAG = -shared -fPIC
    RM = rm -f
    MKDIR = mkdir -p $(1)
    LIB_PREFIX = lib-
endif

CC = gcc

OUT_DIR = ./out/lib
SRC_DIR = ./src/clib

KDTREE_SRC = $(SRC_DIR)/kdtree.c
KDTREE_OUT = $(OUT_DIR)/$(LIB_PREFIX)kdtree.$(EXT)

FACIAL_EMBEDDING_SRC = $(SRC_DIR)/facial_embedding.c
FACIAL_EMBEDDING_OUT = $(OUT_DIR)/$(LIB_PREFIX)facial-embedding.$(EXT)

.PHONY: all clean

all: $(KDTREE_OUT) $(FACIAL_EMBEDDING_OUT)

# Create output directory if needed
$(KDTREE_OUT): $(KDTREE_SRC)
	@$(call MKDIR,$(OUT_DIR))
	$(CC) $(SHARED_FLAG) -o $@ $<

$(FACIAL_EMBEDDING_OUT): $(FACIAL_EMBEDDING_SRC) $(KDTREE_OUT)
	@$(call MKDIR,$(OUT_DIR))
	$(CC) $(SHARED_FLAG) -o $@ $< -L$(OUT_DIR) -l-kdtree

clean:
	$(RM) $(OUT_DIR)/*.$(EXT)
