Dans un sous-dossier nommé **my_strcat** situé à la racine du projet.

Fichiers à rendre :

```
.
└── my_strcat.s

1 directory, 1 file
```

---
Concevoir une implémentation de la fonction strcat, résidant dans le fichier my_strcat.s, conforme au prototype que voici.
```cpp
    char    *my_strcat(char *dst, const char *src);
```
> **Pensez au ``man 3 strcat``.**

- La fonction a le même comportement que son homologue système.

- Vous devez compiler votre code assembleur avec nasm.

- Code 64 bits obligatoire - par extension, la convention d’appel est celle du C 64 bits.  

- La syntaxe Intel est seule employée. 
