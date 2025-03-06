Dans un sous-dossier nommé **my_get_nbr_recurs** situé à la racine du projet.

Fichiers à rendre :

```
.
└── my_get_nbr_recurs.c

1 directory, 1 file
```

---
Écrire un fichier my_get_nbr_recurs.c contenant une fonction:
```cpp
    #ifndef _My_GET_NBR_RECURS_H
    #define _MY_GET_NBR_RECURS_H 1

    extern int my_get_nbr_recurs(char const str[]);

    #endif /* _MY_GET_NBR_RECURS_H */
```
Cette fonction transforme un nombre passé en ``char const []`` et le
renvoie en ``int``.

> **Attention, le ``int`` est un entier signé.**

Par exemple:

* Si str="123", la valeur de retour doit être 123
* Si str="737244", la valeur de retour doit être 737244

> **Cette version doit être récursive, mais une fonction intermédiaire est peut-être nécessaire.**

> **Toutes fonctions non spécifiées sont interdites**
