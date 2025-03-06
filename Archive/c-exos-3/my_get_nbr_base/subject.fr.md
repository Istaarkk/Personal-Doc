À la racine du repository, dans le répertoire **my_get_nbr_base**.

Fichiers à rendre :

```
.
└── my_get_nbr_base.c

1 directory, 1 file
```

---
Écrire un fichier my_get_nbr_base.c contenant une fonction:
```cpp
    #ifndef _MY_GET_NBR_BASE_H
    #define _MY_GET_NBR_BASE_H 1

    extern int my_get_nbr_base(const char num[], const char base[], const char sign);

    #endif /* _MY_GET_NBR_BASE_H */
```
Cette fonction attend en premier paramètre une string représentant un nombre,
 en deuxième paramètre une string représentant une base et en troisième
 paramètre un caractère représentant le signe négatif.

Il faut renvoyer le chiffre correspondant sous forme de `int`.

> **Attention, la ``base`` ainsi que le ``signe`` de négativité peuvent être représentés par n'importe quels caractères**

Par exemple:

* Si num="%123", base="0123456789", char="%" la valeur de retour doit être -123
* Si num="^dab", base="xabcdefg", char="^" la valeur de retour doit être -266

> **La fonction doit retourner 0 si elle tombe sur un caractère qui n'est pas supporté.**

> **Toutes fonctions non spécifiées sont interdites**
