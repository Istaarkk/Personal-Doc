À la racine du repository, dans le répertoire **my_strrev**.

Fichiers à rendre :

```
.
└── my_strrev.s

1 directory, 1 file
```

---
Concevoir une fonction my_strrev, résidant dans le fichier my_strrev.s, qui inverse une séquence de caractères - par exemple, "bonjour" devient "ruojnob".
```cpp
    char *my_strrev(const char *s);
```
- Vous devez compiler votre code assembleur avec nasm.

- Code 64 bits obligatoire - par extension, la convention d’appel est celle du C 64 bits.  

- La syntaxe Intel est seule employée. 

- Vous aurez à utiliser `malloc` pour instancier votre buffeur de retour.
