À la racine du repository, dans le répertoire **my_gen_str**.

Fichiers à rendre :

```
.
└── my_gen_str.c

1 directory, 1 file
```

---
Écrire un fichier my_gen_str.c contenant une fonction:
```cpp
    #ifndef __MY_GEN_STR_H
    #define __MY_GEN_STR_H  1

    extern char* my_gen_str(char * const __format, ...);

    #endif /* __MY_GEN_STR_H */
```
Écrivez une fonction qui va créer une chaine de caractères (alloués dynamiquement)
en se basant sur le paramètre `format` qui contient possiblement des `placeholders`.

Les `placeholders` sont envoyés après le paramètre `format` et dois se terminer par NULL.
Il peut y en avoir un nombre variable de placeholder.

Chaque placeholder a un index correspondant à sa position en tant que paramètre.

Exemple:

    - my_gen_str("coucou", NULL) -> retournée="coucou"
    - my_gen_str("coucou {0}", NULL) -> retournée="coucou "
    - my_gen_str("coucou {1}", NULL) -> retournée="coucou "
    - my_gen_str("coucou {999}", NULL) -> retournée="coucou "
    - my_gen_str("coucou {0}", "test", NULL) ->  retournée="coucou test"
    - my_gen_str("coucou {0} {0}", "test", NULL) ->  retournée="coucou test test"

    - my_gen_str("coucou {1} un {0}", "test", "c'est", NULL)
                ->  retournée="coucou c'est un test"
    - my_gen_str("coucou {{}} {1} {8} {oui} {0} {  0}", "Odd" "superH", NULL)
                -> retournée="coucou {{}} superH  {oui} Odd {  0}"

> **man va_start**
