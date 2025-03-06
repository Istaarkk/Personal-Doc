À la racine du repository, dans le répertoire **my_cat**.

Fichiers à rendre :

```
.
└── my_cat.c

1 directory, 1 file
```

---
Écrire un fichier my_cat.c contenant une fonction prototypée comme cela:
```cpp
    int my_cat(const char *const filename);
```
Écrivez une fonction appelé cat dans un fichier, qui exécute les mêmes tâches que la commande
`cat` de votre système. Vous n'avez pas à gérer les options. Attention
toutefois, si le paramètre de nom de fichier est ``NULL``, vous devez gérer l'entrée standard accessible par le file descripteur `0`.
La fonction retournera ``1`` en cas d'erreur sinon ``0``.
```cpp
    #ifndef _MY_CAT_H
    #define _MY_CAT_H 1

    extern int my_cat(const char *const filename);

    #endif /* _MY_CAT_H */
```
> **Les fonctions ``man 2 open``, ``man 2 read``, ``man 2 write``, ``man 2 close`` sont autorisés.**

> **``stdio.h`` est interdit.**
