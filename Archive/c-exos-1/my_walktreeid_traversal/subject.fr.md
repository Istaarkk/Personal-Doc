Dans un sous-dossier nommé **my_walktreeid_traversal** situé à la racine du projet.

Fichiers à rendre :

```
.
└── my_walktreeid_traversal.c

1 directory, 1 file
```

---
Nous vous donnons un ``.o`` contenant le code pour les fonctions suivantes:
```cpp
    #ifndef __WALKTREEID_H
    #define __WALKTREEID_H

    typedef long int treeid;

    treeid wkt_create(char);
    void wkt_destroy(treeid);

    void wkt_add_left(treeid root, treeid child);
    void wkt_add_right(treeid root, treeid child);
    treeid wkt_get_left(treeid root);
    treeid wkt_get_right(treeid root);
    char wkt_get_char(treeid root);

    #include "walktreeid_traversal.h"

    #endif
```
Ces fonctions permettent de manipuler un arbre binaire abstrait uniquement accessible par des identifiants de type ``treeid`` :

- `wkt_create` crée un noeud nommé par le caractère passé en paramètre et le retourne sous forme de ``treeid``.
- `wkt_destroy` détruit le noeud.
- `wkt_add_left` ajoute au noeud ``root`` le noeud ``child`` a sa gauche. Si la place été déjà prise détruit l'ancien noeud à gauche avant d'ajouter ``child``.
- `wkt_add_right` ajoute au noeud ``root`` le noeud ``child`` a sa droite. Si la place été déjà prise détruit l'ancien noeud à droite avant d'ajouter ``child``.
- `wkt_get_left` retourne le noeud à la gauche de ``root``.
- `wkt_get_right` retourne le noeud à la droite de ``root``.
- `wkt_get_char` retourne le caractère nommant le noeud.

Par exemple, pour créer un arbre nous utiliserons un code suivant:
```cpp
    treeid X = wkt_create('X');
    treeid Y = wkt_create('Y');
    treeid Z = wkt_create('Z');

    wkt_add_left(X, Y);
    wkt_add_right(X, Z);
```
Nous vous demandons de fournir les trois fonctions de parcours récursif suivante:
```cpp
    #ifndef __WALKTREEID_TRAVERSAL_H
    #define __WALKTREEID_TRAVERSAL_H

    void wkt_postorder_show(treeid root);
    void wkt_preorder_show(treeid root);
    void wkt_inorder_show(treeid root);

    #endif
```
Une fonction de parcours récursif est une fonction qui partant de la racine, va accéder à chacune de ses feuilles via une fonction récursive (c'est à dire qui se rappel elle-même).

Ces fonctions parcours l'arbre dans un certain ordre en affichant le noeud parcourus via un ``printf("%c\n", wkt_get_char(node));``

L'arbre peut avoir une taille arbitraire.

Stratégies d'action sur un arbre binaire:

- PRE-ORDER: On traite le noeud en cours puis respectivement sa partie gauche, puis droite.
- POST-ORDER: On traite respectivement la partie gauche, puis droite du noeud en cours, puis finalement celui-ci.
- IN-ORDER: On traite la partie gauche du noeud courant, puis le noeud lui-même, et enfin de sa partie droite.

Ainsi sur l'arbre X, Y, Z on affichera le contenu suivant :

- X puis Y puis Z en PRE-ORDER
- Y puis Z puis X en POST-ORDER
- Y puis X puis Z en IN-ORDER

> **Toutes fonctions non spécifiées sont interdites**
