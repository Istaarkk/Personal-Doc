À la racine du repository, dans le répertoire **my_put_nbr_base**.

Fichiers à rendre :

```
.
└── my_put_nbr_base.c

1 directory, 1 file
```

---
Écrire un fichier my_put_nbr_base.c contenant une fonction, tel que:
```cpp
    char *my_put_nbr_base(int n, const char *base, char sign);   
---
    my_put_nbr_base(12, "0123456789", '-') 
        => "12"
    my_put_nbr_base(12, "01234567", '-') 
        => "14"
    my_put_nbr_base(100, "0123456789ABCDEF", '-') 
        => "64"
    my_put_nbr_base(-100, "0123456789ABCDEF", '-') 
        => "-64"
    my_put_nbr_base(-1217, "TRICHE", 'P') 
        => "PECHE"
```
La chaîne de caractère retourné sera alloué par __my_put_nbr_base__ et devra être libéré par l'appelant.

> **Fonctions autorisés: malloc**
