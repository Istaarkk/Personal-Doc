À la racine du repository, dans le répertoire **my_puts**.

Fichiers à rendre :

```
.
└── my_puts.s

1 directory, 1 file
```

---
Concevoir une implémentation de la fonction puts, résidant dans le fichier my_puts.s, conforme au prototype que voici.
```cpp
    int     my_puts(const char *s);
```
- La fonction a le même comportement que son homologue système.

- L'appel système write est autorisé. 

- Vous devez compiler votre code assembleur avec nasm.

- Code 64 bits obligatoire - par extension, la convention d’appel est celle du C 64 bits.  

- La syntaxe Intel est seule employée. 
