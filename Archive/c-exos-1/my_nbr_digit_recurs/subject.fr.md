Dans un sous-dossier nommé **my_nbr_digit_recurs** situé à la racine du projet.

Fichiers à rendre :

```
.
└── my_nbr_digit_recurs.c

1 directory, 1 file
```

---
Écrire un fichier `my_nbr_digit_recurs.c` contenant une fonction:
```cpp
    #ifndef _MY_NBR_DIGIT_RECURS_H
    #define _MY_NBR_DIGIT_RECURS_H 1

    extern int my_nbr_digit_recurs(int number, int base);

    #endif /* _MY_NBR_DIGIT_RECURS_H */
```
Cette fonction doit retourner le nombre de chiffres utiles pour exprimés la valeur contenu dans
`number` en base `base`. Si des erreurs sont détectées, une valeur
négative doit être retournée.

Quelques exemples:

- Si number=123456 et base=10, le resultat sera 6
- Si number=0 et base=2, le resultat sera 1
- Si number=1 et base=15, le resultat sera 1

Attention toutefois, vous ne pouvez pas utiliser de boucle itérative
(for, while, ...), mais uniquement l'appelle de fonction.

> **Toutes fonctions non spécifiées sont interdites**
