Dans un sous-dossier nommé **my_max** situé à la racine du projet.

Fichiers à rendre :

```
.
└── my_max.s

1 directory, 1 file
```

---
Concevoir une fonction my_max, résidant dans le fichier my_max.s, qui retourne à l'appelant la valeur la plus élevée parmi un ensemble de trois `long int`. 

Le passage de paramètre se fait par registre, respectivement ``rdi``, ``rsi`` et ``rdx``.
La valeur de retour sera stocké dans ``rax``.

- De préférence, employez une instruction de la famille des instructions de déplacement conditionnel  (CMOV)

- Vous devez compiler votre code assembleur avec nasm.

- Code 64 bits obligatoire.

- La syntaxe Intel est seule employée. 

Vous pourrez tester votre code ainsi:
```shell
    user$ gcc my_max.o stub_test.o
    user$ ./a.out
```
