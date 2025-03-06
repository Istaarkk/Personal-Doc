Dans un sous-dossier nommé **my_memcpy** situé à la racine du projet.

Fichiers à rendre :

```
.
└── my_memcpy.s

1 directory, 1 file
```

---
Concevoir une implémentation de la fonction memcpy, résidant dans le fichier my_memcpy.s, conforme au prototype que voici. 
```cpp
    void    *my_memcpy(void *dst, const void *src, unsigned int n);
```
> **Pensez à regarder dans le manifeste pour les opcodes.**

- La fonction a le même comportement que son homologue système.

- Vous devez compiler votre code assembleur avec nasm.

- Code 64 bits obligatoire - par extension, la convention d’appel est celle du C 64 bits.  

- La syntaxe Intel est seule employée. 
