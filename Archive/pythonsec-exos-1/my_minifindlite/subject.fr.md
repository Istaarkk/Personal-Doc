À la racine du repository, dans le répertoire **my_minifindlite**.

Fichiers à rendre :

```
.
└── my_minifindlite

1 directory, 1 file
```

---


Il vous est demandé de réaliser un script python nommé `my_minifindlite` similaire à la commande `find` et supportant seulement certain flag.

Votre commande `my_minifindlite` prendra un PATH puis les paramètres.

SYNOPSIS:

    ./my_minifindlite PATH [options]

Les tests suivants:
- -depth
- -maxdepth levels
- -mindepth levels
- -name pattern
- -path pattern
- -type type

Les actions suivantes:
- -print
- -exec command ;

L'ordre de traitement des fichier/répertoire est lexicographique et non dans l'ordre de création comme un find normal.

> **module autorisés: sys, subprocess, pathlib, fnmatch**

> **il est interdit d'appeler l'utilitaire find par n'importe quel moyen (os.system, subprocess), il faut "réimplémenter" find.**
