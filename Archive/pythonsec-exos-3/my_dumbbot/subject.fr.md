À la racine du repository, dans le répertoire **my_dumbbot**.

Fichiers à rendre :

```
.
└── my_dumbbot

1 directory, 1 file
```

---

Vous devez avoir fini `my_dumbsite` pour aborder cet exercice... ou bien les faire en parallèle car l'un utilise l'autre.

L'objectif est de fournir un script 'my_dumbbot' capable de se connecter sur un site similaire à l'application `my_dumbsite`.
Votre script va de manière automatique insérer des données provenant d'un fichier CSV passé en paramètre dans le formulaire du site.

Le fichier CSV aura le format suivant:

    name;lastname;login;desc
    "albert";"dupond";"albert_dupond";"en recherche d'alternance"

Votre script pourra prendre les options suivantes:

-u URL : (optionnel) on peut préciser l'url et le port de connexion à l'application Flask (http://localhost:5000 par défaut)

-p CSVFILE : (obligatoire) on donne le fichier CSV à lire et à insérer.

Comme dans l'exemple des slides du cours, vous utiliserez un [webdriver-manager pour Firefox](https://pypi.org/project/webdriver-manager).

> **module autorisés: selenium, webdriver-manager, tous les modules standards et builtin**
