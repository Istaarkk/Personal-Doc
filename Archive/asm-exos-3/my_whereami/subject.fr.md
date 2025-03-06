À la racine du repository, dans le répertoire **my_whereami**.

Fichiers à rendre :

```
.
└── my_whereami.s

1 directory, 1 file
```

---
Concevoir une fonction my_whereami, résidant dans le fichier my_whereami.s, avec le prototype que voici :
```cpp
    int64_t my_whereami(int64_t *where);
```
- my_whereami renvoie le nombre d'octets dont elle se compose.
- my_whereami doit renseigner son addresse via son paramètre where.

- Vous devez compiler votre code assembleur avec nasm.

- Code 64 bits obligatoire - par extension, la convention d’appel est celle du C 64 bits.  

- La syntaxe Intel est seule employée. 
