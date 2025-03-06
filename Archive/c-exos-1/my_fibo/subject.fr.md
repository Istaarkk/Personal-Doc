Dans un sous-dossier nommé **my_fibo** situé à la racine du projet.

Fichiers à rendre :

```
.
└── my_fibo.c

1 directory, 1 file
```

---
Écrivez un fonction qui calcule la *suite de Fibonacci* de manière récursive comme expliqué [ici](https://fr.wikipedia.org/wiki/Suite_de_Fibonacci).
```cpp
    #ifndef _MY_FIBO_H
    #define _MY_FIBO_H 1

    extern unsigned long my_fibo(unsigned long __n);

    #endif /* _MY_FIBO_H */
```
La fonction prends en paramètre le rang de la fonction de fibonacci.

Ainsi `my_fibo(15)` sera égale à 610.

> **Toutes fonctions non spécifiées sont interdites**
