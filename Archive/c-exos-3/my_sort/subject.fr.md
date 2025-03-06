À la racine du repository, dans le répertoire **my_sort**.

Fichiers à rendre :

```
.
└── my_sort.c

1 directory, 1 file
```

---
Écrire un fichier my_sort.c contenant une fonction:
```cpp
    #ifndef _MY_SORT_H
    #define _MY_SORT_H 1

    extern void my_sort(int arr[], unsigned int length);

    #endif /* _MY_SORT_H */
```
Cette fonction trie un tableau de nombre dans l'ordre croissant.

Le paramètre est passé par référence, car le tableau en mémoire n'est pas dupliqué. Ainsi vous pouvez modifier le tableau envoyé.

> **Toutes fonctions non spécifiées sont interdites.**
