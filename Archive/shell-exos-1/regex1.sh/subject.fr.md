Dans un sous-dossier nommé **regex1.sh** situé à la racine du projet.

Fichiers à rendre :

```
.
└── regex1.sh

1 directory, 1 file
```

---
Ecrire un script shell nommé ``regex1.sh`` avec les droits d'exécution correctement positionné, tel que:
```shell
    user$ ./regex1.sh 'command 12' | cat -e
    INT 12$
    user$ ./regex1.sh 'command 12tutu' | cat -e
    Unknown$
    user$ ./regex1.sh 'command cool' | cat -e
    LOWER cool$
    user$ ./regex1.sh 'command cool la vie' | cat -e
    Unknown$
    user$ ./regex1.sh 'command _chaussette23' | cat -e
    IDENT _chaussette23$
    user$ ./regex1.sh 'command Cool' | cat -e
    IDENT Cool$
    user$ ./regex1.sh 'command "comment va?"' | cat -e
    STR comment va?$
    user$ ./regex1.sh 'command "\"Hello World\""' | cat -e
    STR "Hello World"$
```
