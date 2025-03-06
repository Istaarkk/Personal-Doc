Dans un sous-dossier nommé **my_revstr** situé à la racine du projet.

Fichiers à rendre :

```
.
└── my_revstr.c

1 directory, 1 file
```

---
Écrire un fichier my_revstr.c contenant une fonction:
```cpp
    #ifndef _My_REVSTR_H
    #define _MY_REVSTR_H 1

    extern void my_revstr(char str[]);

    #endif /* _MY_REVSTR_H */
```
Cette fonction doit inverser une chaîne de caractère.

L'inversion est dite "en place", car la chaîne en mémoire n'est pas dupliqué. Ainsi vous de pouvez pas retourner de nouvelle chaîne de caractère.

> **Toutes fonctions non spécifiées sont interdites**
