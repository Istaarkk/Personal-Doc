À la racine du repository, dans le répertoire **my_split**.

Fichiers à rendre :

```
.
└── my_split.c

1 directory, 1 file
```

---
Vous devez écrire un fichier `my_split.c` contenant une fonction 'my_split', tel que :
```cpp
    #ifndef _MY_SPLIT_H
    #define _MY_SPLIT_H 1

    extern char **my_split(const char * const str, const char * const sep);

    #endif /* _MY_SPLIT_H */
```
La fonction 'my_split' découpe la chaîne 'str' en N sous-chaîne de caractère et
retourne un tableau de chaîne de caractère permettant d'accéder à ces
sous-chaînes. Chaque sous-chaîne de caractère a été dynamiquement alloué ainsi
que le tableau retourné. Le tableau retourné contient N+1 élément dont le
dernier contient un pointeur NULL.

Le découpage se fait lorsqu'on rencontre un des caractères de 'sep' (pour separator).

quelques exemples :

* my_split("A|B|C", "|"); équivalent à {"A", "B", "C", 0};
* my_split("A|B|C,D,E|F,G", "|,"); équivalent à {"A", "B", "C", "D", "E", "F", "G", 0};
* my_split("A,,C,D", ","); équivalent à {"A", "", "C", "D", 0};
* my_split(",|", ",|"); équivalent à {"", "", "", 0};

> **fonctions autorisés: malloc**
