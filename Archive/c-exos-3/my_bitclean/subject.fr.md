À la racine du repository, dans le répertoire **my_bitclean**.

Fichiers à rendre :

```
.
└── my_bitclean.c

1 directory, 1 file
```

---
Écrire un fichier `my_bitclean.c` contenant une fonction:
```cpp
    #ifndef _MY_BITCLEAN_H
    #define _MY_BITCLEAN_H	1

    #include <stddef.h>
    #include <stdint.h>

    extern uint32_t my_bitclean(uint32_t __bitmap, int __pos);

    #endif /* _REF_MY_BITCLEAN_H */
```
Cette fonction éteint un bit de la valeur du premier argument (entier 32 bit non signé) à la position pos (commençant à 0) et retourne la valeur.

Attention toutefois:

* Si pos est négatif, vous devez partir du bit de poids fort
* Si pos est positif, vous devez partir du bit de poids faible
* Si pos est égal à 0, vous devez rendre la valeur de retour multiple de 2

Par exemple:

* Si valeur=7 et que pos=2, la valeur de retour doit être 3
* Si valeur=103 et que pos=6, la valeur de retour doit être 39
* Si valeur=8542 et que pos=-18, la valeur de retour doit être 350
