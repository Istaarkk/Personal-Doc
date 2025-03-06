À la racine du repository, dans le répertoire **my_rle**.

Fichiers à rendre :

```
.
└── my_rle.c

1 directory, 1 file
```

---
Le format d'encodage RLE est utilisé pour compresser des textes. Cela consiste a détecté les occurrences successives d'un même caractère et de les substituer par le nombre d'occurrence suivi du caractère répéter. Le format demandé ici ne pourra encodé au maximum que 9 caractères successifs.

exemples:

* rle_encode("AAAAAAACBBBBBB") => "7A1C6B"
* rle_decode("9A6A") => "AAAAAAAAAAAAAAA"

Chacunes des fonctions retournes une chaîne de caractère nouvellement alloués.
Vous devez écrire un fichier rle.c contenant 2 fonctions en C, tel que:
```cpp
    #ifndef _RLE_H
    #define _RLE_H

    char *rle_encode(const char *s);
    char *rle_decode(const char *s);

    #endif
```
> **Fonctions autorisés: malloc**
