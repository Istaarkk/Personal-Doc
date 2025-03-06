Dans un sous-dossier nommé **my_bsr** situé à la racine du projet.

Fichiers à rendre :

```
.
└── bsr.s

1 directory, 1 file
```

---
Concevoir une fonction my_bsr, résidant dans le fichier bsr.s, qui fait appel à l’instruction BSR de sorte à récupérer le bit le plus significatif d’une valeur donnée. 

Le passage de paramètre se fait par registre, ici ``rdi``.
La valeur de retour sera stockée dans ``rax``.

- Vous devez compiler votre code assembleur avec nasm.

- Code 64 bits obligatoire.

- La syntaxe Intel est seule employée. 

Vous pourrez tester votre code ainsi:
```shell
    user$ gcc bsr.o stub_test.o
    user$ ./a.out
```
