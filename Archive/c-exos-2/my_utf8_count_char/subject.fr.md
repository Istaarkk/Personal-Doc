Dans un sous-dossier nommé **my_utf8_count_char** situé à la racine du projet.

Fichiers à rendre :

```
.
└── my_utf8_count_char.c

1 directory, 1 file
```

---
Écrire un fichier my_utf8_count_char.c contenant une fonction:
```cpp
    #ifndef _MY_UTF8_COUNT_CHAR_H
    #define _MY_UTF8_COUNT_CHAR_H

    extern int my_utf8_count_char(const char *);

    #endif /* _MY_UTF8_COUNT_CHAR_H */
```
Cette fonction compte le nombre de caractère UTF8 que comporte une chaîne de caractère passé en paramètre.

Par exemple:

* Si str pointe vers "la chaîne est trés bien encodé", la valeur de retour doit être 30
* Si str pointe vers "♚ move to B12 take ♙", la valeur de retour doit être 20 (* utf-8 symbol: black king chess & white chess pawn)
* Si str pointe vers "earing 🎵", la valeur de retour doit être 8 (* utf-8 symbol: musical note)

Cette version **doit être itérative**.

> **Toutes fonctions non spécifiées sont interdite**s
