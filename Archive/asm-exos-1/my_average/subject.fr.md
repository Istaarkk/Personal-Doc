Dans un sous-dossier nommé **my_average** situé à la racine du projet.

Fichiers à rendre :

```
.
└── my_average.s

1 directory, 1 file
```

---
Concevoir une fonction assembleur ``my_average``, résidant dans le fichier my_average.s, qui retourne à l'appelant la moyenne de quatre nombres.

Le passage de paramètre se fait par registre, respectivement ``rdi``, ``rsi``, ``rdx``, et ``rcx``.
La valeur de retour sera stockée dans ``rax``.

- Vous devez compiler votre code assembleur avec nasm.

- Code 64 bits obligatoire.

- La syntaxe Intel est seule employée. 

Vous pourrez tester votre code ainsi:
```shell
    user$ gcc my_average.o stub_test.o
    user$ ./a.out
```
