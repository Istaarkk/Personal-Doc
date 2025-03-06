Dans un sous-dossier nommé **my_eratosthenes** situé à la racine du projet.

Fichiers à rendre :

```
.
└── my_eratosthenes.c

1 directory, 1 file
```

---
Ecrire une fonction qui calcul et affiche sur la sortie standard la liste des nombres premier compris entre 0 et ``n`` inclus passé en paramètre par le crible d’eratoshenes.

``n`` ne pourra pas être supérieur à 1000.

Si une valeur plus grande que 1000 est envoyé la fonction retourne sans rien afficher.
```cpp
    #ifndef _MY_ERATOSTHENES_H
    #define _MY_ERATOSTHENES_H 1

    extern void my_eratosthenes(int n);

    #endif /* _MY_ERATOSTHENES_H */
```
Nous aurons notre propre ``main`` pour la correction.
```shell
    user$ ./a.out | head -10
    2
    3
    5
    7
    11
    13
    17
    19
    23
    29
```
