Dans un sous-dossier nommé **my_alphabet** situé à la racine du projet.

Fichiers à rendre :

```
.
└── my_alphabet.c

1 directory, 1 file
```

---
Écrire un fichier my_alphabet.c contenant une fonction:
```cpp
    #ifndef _MY_ALPHABET_H
    #define _MY_ALPHABET_H 1

    extern int my_alphabet(void);

    #endif /* _MY_ALPHABET */
```
Cette fonction doit afficher toutes les lettres de l'alphabet sans retour à la
ligne tout en renvoyant le nombre de caractères affiché.

L'affichage se fera via la fonction ``write``.

> **ATTENTION: Déclarer une chaine `char alpha[] = "abcdefghijklmnopqrstuvwxyz" n'est pas autorisée`**

> **N'oubliez pas le ``man 2 write``**

> **Toutes fonctions non spécifiées sont interdites**
