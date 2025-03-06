Dans un sous-dossier nommé **my_countv** situé à la racine du projet.

Fichiers à rendre :

```
.
└── my_countv.s

1 directory, 1 file
```

---
Concevoir une fonction my_countv, résidant dans le fichier my_countv.s, qui compte le nombre de voyelles qu'incorpore une séquence de caractères. 
```cpp
    void my_countv(char s[], int size, int v[6]);
```
Au retour de la fonction, la variable v de type tableau est initialisé avec le nombre d'occurrences de la lettre 'a' (v[0]), de la lettre 'e' (v[1]), de la lettre 'i' (v[2]), et ainsi de suite jusque v[5] pour 'y'.

- Pour des raisons de concision du code, seules les lettres minuscules sont prises en compte.

- Vous devez compiler votre code assembleur avec nasm.

- Code 64 bits obligatoire - par extension, la convention d’appel est celle du C 64 bits.  

- La syntaxe Intel est seule employée. 
