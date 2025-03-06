À la racine du repository, dans le répertoire **my_str_replace**.

Fichiers à rendre :

```
.
└── my_str_replace.c

1 directory, 1 file
```

---
Vous devez écrire un fichier my_str_replace.c contenant une fonction 'my_str_replace':
```cpp
    #ifndef __MY_STR_REPLACE_H
    #define __MY_STR_REPLACE_H

    char *my_str_replace(const char *old_pat, const char *str, const char *new_pat);

    #endif
```
Fichier à rendre dans une chaîne de caractère nouvellement alloués copie de la chaine 'str' dans laquelle chaque occurrence de 'old_pat' est remplacé par 'new_pat', tel que:
```cpp
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include "my_str_replace.h"

    void check(const char *o, const char *s, const char *n, const char *cmp)
    {
    char *res = str_replace(o, s, n);
    if (!strcmp(res, cmp))
        printf("OK %s\n", res);
    free(res);
    }

    int main(void)
    {
    check("o", "bobo", "", "bb");
    check("o", "bobo", "i", "bibi");
    check("o", "bobo", "oo", "booboo");
    check("", "bobo", "a", "bobo");
    check("bo", "bobo", "k", "kk");
    check("bo", "bobo", "be", "bebe");
    check("bobo", "bobo", "bubu", "bubu");
    check("bobobo", "bobo", "bubu", "bobo");
    return 0;
    }
```
* Si 'old_pat' est NULL, 'my_str_replace' insérera 'new_pat' entre tous les caractères de str sans oublier avant le premier caractère et après le dernier.
* Si 'new_pat' est NULL, chaque occurrence de 'old_pat' sera supprimé de la nouvelle chaîne.
* Si 'str' est NULL, 'my_str_replace' retourne NULL.

Les substitutions s'opère successivement de la gauche vers la droite dans une nouvelle chaîne. Il n'y a pas de substitution récursive dans la nouvelle chaîne. exemples:
```cpp
    my_str_replace("bo", "bobo", "babo") 
        => "babobabo"
    my_str_replace("", "bobo", "a") 
        => "abaoabaoa"
```
