Dans un sous-dossier nommé **my_echo** situé à la racine du projet.

Fichiers à rendre :

```
.
└── my_echo.c

1 directory, 1 file
```

---
Écrire un fichier `my_echo.c` contenant une fonction:
```cpp
    #ifndef _MY_ECHO_H
    #define _MY_ECHO_H 1

    extern void my_echo(char const str[]);

    #endif /* _MY_ECHO_H */
```
Vous devez afficher la chaine de caractères qui vous aient envoyé par argument.
L'affichage doit être réalisé caractères par caractère via la fonction
`static inline void my_putchar(char n)` qui vous est fourni dans un header
`my_putchar.h`

La fonction doit avoir le même comportement que la commande `echo` de bash.
```cpp
    #ifndef _MY_PUTCHAR_H
    #define _MY_PUTCHAR_H 1
    #include <unistd.h>

    static inline void my_putchar(char c)
    {
        write(STDOUT_FILENO, &c, 1);
    }

    #endif /* _MY_PUTCHAR_H */
```
> **Toutes fonctions non spécifiées sont interdites**
