#ifndef KODEX_FACOM_KDTREE_H
#define KODEX_FACOM_KDTREE_H

typedef struct _node {
    void * key;
    node_t * left;
    node_t * right;
} node_t;

typedef struct _tree {
    node_t * root;
    int (*cmp)(void *, void *, int);
    double (*dist) (void *, void *);
    int k;
} tree_t;

void kdtree_build(tree_t * arv, int (* cmp)(void *a, void *b, int), double (* dist) (void *, void *), int k);
void kdtree_insert(tree_t * arv, void * key);
void kdtree_destroy(tree_t * arv);
node_t * kdtree_search_nearest(tree_t * arv, void * key);

#endif
