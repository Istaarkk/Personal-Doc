À la racine du repository, dans le répertoire **my_fillstruct**.

Fichiers à rendre :

```
.
└── my_fillstruct.s

1 directory, 1 file
```

---
Concevoir une fonction my_fillstruct, résidant dans le fichier my_fillstruct. my_fillstruct est chargée d'assigner les valeurs d'une structure donnée.  La fonction est conforme au prototype que voici :
```cpp
    void	my_fillstruct(struct _my_struct *, int64_t, double);

    struct _my_struct { int64_t i; double d; };
```
- L'instruction FLD, apparentée à la manipulation des nombres flottants, est obligatoire. Attention à la convention d'appel !!!

- Vous devez compiler votre code assembleur avec nasm.

- Code 64 bits obligatoire - par extension, la convention d’appel est celle du C 64 bits.  

- La syntaxe Intel est seule employée. 
