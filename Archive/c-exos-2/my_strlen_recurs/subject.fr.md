Dans un sous-dossier nommé **my_strlen_recurs** situé à la racine du projet.

Fichiers à rendre :

```
.
└── my_strlen_recurs.c

1 directory, 1 file
```

---
Écrire un fichier my_strlen_recurs.c contenant une fonction:
```cpp
    #ifndef _MY_STRLEN_RECURS_H
    #define _MY_STRLEN_RECURS_H 1

    extern int my_strlen_recurs(char const str[]);

    #endif /* _MY_STRLEN_RECURS_H */
```
Cette fonction compte le nombre de caractère que comporte un tableaux de char[].

Quelques exemples:

* Si str="salut a tous", la valeur de retour doit être 12
* Si str="g@m3rz", la valeur de retour doit être 6
* Si str="", la valeur de retour doit être 0

> **Attention toutefois, vous ne pouvez pas utiliser de boucle itérative (for, while, ...), mais uniquement l'appel de fonction.**

> **Toutes fonctions non spécifiées sont interdites**
