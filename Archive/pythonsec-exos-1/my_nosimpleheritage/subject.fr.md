À la racine du repository, dans le répertoire `my_nosimpleheritage`.

Fichiers à rendre :

```
 .
 └── my_nosimpleheritage.py
```

---

L'objectif de cet exercice est de vous faire aborder les aspects relatifs à la conception orientée objet.

Vous implémenterez un module python qui contiendra plusieurs classes respectant les spécifications suivantes:

- Écrire une classe de base nommée `Vehicule`. Le constructeur prenant un paramètre entier nommé `porte`, avec valeur par défaut à 2.
- Écrire une classe de base nommée `Animal`. Le constructeur prenant 1 paramètre entier nommé `patte`, et 1 paramètre booléen nommé `queue`, avec valeur par défaut respectivement 4 et False.

- Écrire une classe de base abstraite nommée `Deplacement`, avec une méthode abstraite `move_to` prenant 3 paramètres annotés `float` x, y, z et un paramètre zone annoté comme une string.
Le fait de se déplacer, implique pour les classes qui hériteront de cette capacité qu'elles implémentent ces propriétés abstraites x, y, z initialisées à 0.0 dans la classe concrète.

- Écrire une classe de base `Volant` fille de `Deplacement`, implémentant `move_to` et retournant:
        f"se déplace vers {x}, {y}, {z} en volant". Vérifier que `z` est positif, sinon lever une exception.

- Écrire une classe de base `Courant` fille de `Deplacement`, implémentant `move_to` et retournant:
        f"se déplace vers {x}, {y} en courant". Vérifier que `z` est nulle et que `zone` vaut 'terre', sinon lever une exception.

- Écrire une classe de base `Marchant` fille de `Deplacement`, implémentant `move_to` et retournant:
        f"se déplace vers {x}, {y} en marchant". Vérifier que `z` est nulle et que `zone` vaut 'terre', sinon lever une exception.

- Écrire une classe de base `Roulant` fille de `Deplacement`, implémentant `move_to` et retournant:
        f"se déplace vers {x}, {y} en roulant". Vérifier que `z` est nulle et que `zone` vaut 'terre', sinon lever une exception.

- Écrire une classe de base `Flottant` fille de `Deplacement`, implémentant `move_to` et retournant:
        f"se déplace vers {x}, {y} en flottant". Vérifier que `z` est nulle et que `zone` vaut 'mer', sinon lever une exception.

- Écrire une classe de base `Nageant` fille de `Deplacement`, implémentant `move_to` et retournant:
        f"se déplace vers {x}, {y}, {z} en nageant". Vérifier que `z` est négatif et que `zone` vaut 'mer', sinon lever une exception.

- Écrire les classes suivantes en respectant le sens commun pour les héritages multiples:
    - Humain
    - VoitureSansPermis
    - Berline
    - Moto
    - Hors_Bord
    - Spitfire
    - Cygne
    - Canard
    - Poisson

Certaines classes peuvent avoir plusieurs possibilités de déplacement.
Pour savoir laquelle est la plus adaptée au contexte, elles devront essayer et échouer puis tester autre chose.
On préférera la course à la marche si la distance est comprise entre 2.0 et 10.0, l'inverse dans les autres cas.
On considèrera le cygne trop gros pour évoluer sur la terre.

> **module autorisés: abc, math**
