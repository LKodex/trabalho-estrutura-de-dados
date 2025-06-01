#include <stdlib.h>
#include "./headers/kdtree.h"

#define MAX_UID_LENGTH 100
#define MAX_EMBEDDING_LENGTH 128

typedef struct _embedding_reg {
    char uid[MAX_UID_LENGTH];
    double embedding[MAX_EMBEDDING_LENGTH];  
} embedding_reg;

int embedding_cmp(void * left, void * right, int pos)
{
    double diff = ((embedding_reg *) left)->embedding[pos] - ((embedding_reg *) right)->embedding[pos];
    if (diff > 0) return 1;
    if (diff < 0) return -1;
    return 0;
}

double embedding_dist(void * left, void * right){
    double distance = 0;
    for (int i = 0; i < MAX_EMBEDDING_LENGTH; i++) {
        double diff = ((embedding_reg *) left)->embedding[i] - ((embedding_reg *) right)->embedding[i];
        distance += diff * diff;
    }
    return distance;
}

tree_t global_tree;

tree_t * facial_embedding_get_tree() {
    return &global_tree;
}

void facial_embedding_build_tree()
{
    global_tree.k = 2;
    global_tree.dist = embedding_dist;
    global_tree.cmp = embedding_cmp;
    global_tree.root = NULL;
}

void facial_embedding_insert_reg(embedding_reg reg) {
    embedding_reg * new = malloc(sizeof(embedding_reg));
    *new = reg;
    kdtree_insert(&global_tree, new);
}

embedding_reg facial_embedding_search_nearest(embedding_reg query) {
    node_t * nearest = kdtree_search_nearest(&global_tree, &query);
    embedding_reg reg = *((embedding_reg *)(nearest->key));
    return reg;
}
