Dans un sous-dossier nommé **my_strlen** situé à la racine du projet.

Fichiers à rendre :

```
.
└── my_strlen.c

1 directory, 1 file
```

---
Écrire un fichier my_strlen.c contenant une fonction:

```cpp
    #ifndef _MY_STRLEN_H
    #define _MY_STRLEN_H 1

    extern int my_strlen(char const str[]);

    #endif /* _MY_STRLEN_H */
```

Cette fonction compte le nombre de caractère que comporte un tableaux de char[].

Par exemple:

* Si str="salut a tous", la valeur de retour doit être 12
* Si str="g@m3rz", la valeur de retour doit être 6
* Si str="", la valeur de retour doit être 0

Cette version **doit être itérative**.

> **Toutes fonctions non spécifiées sont interdites**
