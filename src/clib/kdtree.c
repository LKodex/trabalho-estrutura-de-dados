#include <stdio.h>
#include <stdlib.h>
#include <float.h>
#include <string.h>
#include <assert.h>
#include "./headers/kdtree.h"

/*Definições desenvolvedor usuario*/
typedef struct _test_reg {
    int lat;
    int lon;
    char nome[100];
} test_reg_t;

void * malloc_test_reg_t(int lat, int lon, char nome[]){
    test_reg_t * reg;
    reg = malloc(sizeof(test_reg_t));
    reg->lat = lat;
    reg->lon = lon;
    strcpy(reg->nome,nome);
    return reg;
}

int test_reg_cmp(void *a, void *b, int pos){
    int ret;
    if (pos == 0) {
        ret = ((test_reg_t *)a)->lat - ((test_reg_t *)b)->lat;
    } else if (pos == 1) {
        ret = ((test_reg_t *)a)->lon - ((test_reg_t *)b)->lon;
    }
    return ret;
}

double test_reg_dist(void * left, void *right){
    double ret_lat = ((test_reg_t *)left)->lat - ((test_reg_t *)right)->lat;
    double ret_lon = ((test_reg_t *)left)->lon - ((test_reg_t *)right)->lon;
    return ret_lat*ret_lat + ret_lon*ret_lon;
}

/*funções desenvolvedor da biblioteca*/

void kdtree_build(tree_t * arv, int (*cmp)(void *a, void *b, int ),double (*dist) (void *, void *),int k){
    arv->root = NULL;
    arv->cmp = cmp;
    arv->dist = dist;
    arv->k = k;
}

/*teste*/
void test_kdtree_build(){
    /* declaracao de variaveis */
    tree_t arv;
    node_t node1;
    node_t node2;

    node1.key = malloc_test_reg_t(2,3,"Dourados");
    node2.key = malloc_test_reg_t(1,1,"Campo Grande");


    /* chamada de funções */
    kdtree_build(&arv,test_reg_cmp,test_reg_dist,2);
    
    /* testes */
    assert(arv.root == NULL);
    assert(arv.k == 2);
    assert(arv.cmp(node1.key,node2.key,0) == 1);
    assert(arv.cmp(node1.key,node2.key,1) == 2);
    assert(strcpy(((test_reg_t *)node1.key)->nome,"Dourados"));
    assert(strcpy(((test_reg_t *)node2.key)->nome,"Campo Grande"));
    free(node1.key);
    free(node2.key);
}

void _kdtree_insert(node_t **root, void * key, int (*cmp)(void *a, void *b, int),int profund, int k){
    if(*root == NULL){
        *root = malloc(sizeof(node_t));
        (*root)->key = key;
        (*root)->left = NULL;
        (*root)->right = NULL;
        return;
    }
    int pos = profund % k;
    if (cmp( (*(*root)).key , key ,pos) <0) {
        _kdtree_insert( &((*(*root)).right), key, cmp, profund + 1, k);
    } else {
        _kdtree_insert( &((*root)->left), key, cmp, profund +1, k);
    }
}

void kdtree_insert(tree_t *arv, void *key){
    _kdtree_insert(&(arv->root),key,arv->cmp,0,arv->k);
}


void _kdtree_destroy(node_t * node){
    if (node!=NULL){
        _kdtree_destroy(node->left);
        _kdtree_destroy(node->right);
        free(node->key);
        free(node);
    }
}

void kdtree_destroy(tree_t *arv){
    _kdtree_destroy(arv->root);
}

void _kdtree_search_nearest(tree_t *arv, node_t ** atual, void * key, int profund, double *menor_dist, node_t **menor){
    if (*atual == NULL) return;
    node_t ** lado_principal; 
    node_t ** lado_oposto;    
    double dist_atual = arv->dist((*atual)->key, key);
    if (dist_atual < *menor_dist){
        *menor_dist = dist_atual;
        *menor = *atual;
    }
    int pos = profund % arv->k;
    int comp = arv->cmp(key, (*atual)->key, pos);
    
    /* define lado principal para buscar */
    if (comp < 0){
        lado_principal =  &((*atual)->left);
        lado_oposto    =  &((*atual)->right); 
    }else{
        lado_principal =  &((*atual)->right);
        lado_oposto    =  &((*atual)->left); 
    }

    _kdtree_search_nearest(arv, lado_principal, key, profund + 1, menor_dist, menor);

    /* Verifica se deve buscar também no outro lado*/

    if (comp*comp < *menor_dist) {
        _kdtree_search_nearest(arv, lado_oposto, key, profund + 1, menor_dist, menor);
    }
}

node_t * kdtree_search_nearest(tree_t *arv, void * key){
    double menor_dist = DBL_MAX;
    node_t * menor = NULL;
    _kdtree_search_nearest(arv,&(arv->root),key,0,&menor_dist,&menor);
    return menor;
}

void test_kdtree_search_nearest(){
    tree_t arv;
    kdtree_build(&arv,test_reg_cmp,test_reg_dist,2);
    kdtree_insert(&arv,malloc_test_reg_t(10,10,"a"));
    kdtree_insert(&arv,malloc_test_reg_t(20,20,"b"));
    kdtree_insert(&arv,malloc_test_reg_t(1,10,"c"));
    kdtree_insert(&arv,malloc_test_reg_t(3,5,"d"));
    kdtree_insert(&arv,malloc_test_reg_t(7,15,"e"));
    kdtree_insert(&arv,malloc_test_reg_t(4,11,"f"));
    node_t * root = arv.root;
    assert(strcmp(((test_reg_t *)root->right->key)->nome, "b")==0);
    assert(strcmp(((test_reg_t *)root->left->key)->nome, "c")==0);
    assert(strcmp(((test_reg_t *)root->left->left->key)->nome, "d")==0);
    assert(strcmp(((test_reg_t *)root->left->right->key)->nome, "e")==0);

    printf("\n");
    test_reg_t  * atual = malloc_test_reg_t(7,14,"x");
    node_t * mais_proximo = kdtree_search_nearest(&arv,atual);
    assert(strcmp(((test_reg_t *)mais_proximo->key)->nome,"e") == 0);

    printf("\n");
    atual->lat = 9;
    atual->lon = 9;
    mais_proximo = kdtree_search_nearest(&arv,atual);
    assert(strcmp(((test_reg_t *)mais_proximo->key)->nome,"a") == 0);

    printf("\n");
    atual->lat = 4;
    atual->lon = 5;
    mais_proximo = kdtree_search_nearest(&arv,atual);
    assert(strcmp(((test_reg_t *)mais_proximo->key)->nome,"d") == 0);

    printf("\n");
    atual->lat = 4;
    atual->lon = 9;
    mais_proximo = kdtree_search_nearest(&arv,atual);
    assert(strcmp(((test_reg_t *)mais_proximo->key)->nome,"f") == 0);

    free(atual);
    kdtree_destroy(&arv);
}

int main(void){
    test_kdtree_build();
    test_kdtree_search_nearest();
    printf("SUCCESS!!\n");
    return EXIT_SUCCESS;
}
