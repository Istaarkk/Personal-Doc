Dans un sous-dossier nommé **my_hanoi** situé à la racine du projet.

Fichiers à rendre :

```
.
└── my_hanoi.c

1 directory, 1 file
```

---
Explication des puzzles d'Hanoï
-------------------------------

La tour de Hanoï est un puzzle mathématique où nous avons trois tiges et n
disques. L'objectif du puzzle est de déplacer la pile entière vers une autre
tige, en obéissant aux règles simples suivantes :

    1. Un seul disque peut être déplacé à la fois.
    2. Chaque déplacement consiste à prendre le disque supérieur de l'une des
        piles et à le placer au-dessus d'une autre pile, c'est-à-dire qu'un
        disque ne peut être déplacé que s'il s'agit du disque le plus haut d'une
        pile.
    3. Aucun disque ne peut être placé sur un disque plus petit.

Le prototype est le suivant:
```cpp
    #ifndef _MY_HANOI_H
    #define _MY_HANOI_H 1

    extern void my_hanoi(unsigned n);

    #endif /* _MY_HANOI_H */%
```
Ce que vous devez réaliser
-------------------------

Vous devez créer un fichier `my_hanoi.c` qui prendra en paramètre le nombre de
disques et devra écrire dans la sortie standard (notation fléché avec retour chariot) tous les mouvements pour
déplacer la pile, qui sera toujours sur la tige 1, vers la tige 3 (il n'y aura toujours que 3 tiges).

Exemple avec `n` à 2 (my_hanoi(2)):

    1->2
    1->3
    2->3

On indique seulement un mouvement du disque de la tige 1, 2 ou 3 vers la tige 1, 2 ou 3.

Fonctions authorisées :
    * putchar(char)

> **Toutes fonctions non spécifiées sont interdites**
