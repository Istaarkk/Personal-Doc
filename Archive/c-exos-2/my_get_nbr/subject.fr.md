Dans un sous-dossier nommé **my_get_nbr** situé à la racine du projet.

Fichiers à rendre :

```
.
└── my_get_nbr.c

1 directory, 1 file
```

---
Écrire un fichier my_get_nbr.c contenant une fonction:
```cpp
    #ifndef _My_GET_NBR_H
    #define _MY_GET_NBR_H 1

    extern int my_get_nbr(char const str[]);

    #endif /* _MY_GET_NBR_H */
```
Cette fonction transforme un nombre passé en ``char const []`` et le
renvoie en ``int``.

> **Attention, le ``int`` est un entier signé.**

Par exemple:

* Si str="123", la valeur de retour doit être 123
* Si str="737244", la valeur de retour doit être 737244
* Si str="-2600", la valeur de retour doit être -2600

> **La fonction doit retourner 0 si elle tombe sur un caractère qui n'est pas supporté.*

> **Toutes les fonctions non spécifiées sont interdites**
