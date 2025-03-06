À la racine du repository, dans le répertoire `my_jdr`.

Fichiers à rendre :

```
 .
 └── my_jdr.py

```

---

Vous est donné le fichier *my_jdr.py* qu'il va falloir compléter. Notre objectif est de simuler des dés de jeu de rôle,
et notamment pour gérer le jet de poignée de dés bizarre (de 4 à 20 faces).

Pour comprendre ce que l'on vous donne, il faudra regarder le module python **random**, la surcharge d'opérateur, la surcharge de la fonction **repr** et les fonctions génératrices (statement **yield**) et enfin les **lambda**.

Pool
-----
Vous devez compléter la classe **Pool**, et les classes de dés D6, D8, D10, D12, D20 (en s'inspirant du D4 fournit dans le *my_jdr.py*).
Ainsi que les instances standard d4, d6, d8, ..., d20 pour tout type de dés.

Complétez le fichier *my_jdr.py* tel que (hé oui, un bout de code est aussi une spécification) :

```python

    from my_jdr import *

    p1 = D6() + d6 + 1
    print(repr(p1))

    p2 = d6 * 4 + 12 + 4 * d8
    print(repr(p2))

    AbstractResult.seed(XXXXX)  # XXXXX sera donné par la correction
    print(p1.throw())
    print(p2.throw())
    print(p1.show())
    print(p2.show())

    if type(p1.roll()).__name__ != 'generator':
        raise TypeError('la methode roll doit retourner un generateur')

    for t in (D6() + D4()).roll():
        print(t)
```

Produira le résultat suivant :

```shell

    D6 + D6 + 1
    4D6 + 12 + 4D8
    8
    42
    6, 1, 1
    1, 6, 3, 2, 12, 4 , 1, 5, 8
    (1, 1)
    (1, 2)
    (1, 3)
    (1, 4)
    (2, 1)
    (2, 2)
    (2, 3)
    (2, 4)
    (3, 1)
    (3, 2)
    (3, 3)
    (3, 4)
    (4, 1)
    (4, 2)
    (4, 3)
    (4, 4)
    (5, 1)
    (5, 2)
    (5, 3)
    (5, 4)
    (6, 1)
    (6, 2)
    (6, 3)
    (6, 4)
```

Voir surcharge des opérateurs ([3.3.8. Emulating numeric types](https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types) de *The Python Language Reference / Data Model*).

Infos
------

* Une expression comprenant des dés est un Pool. Ex : D4 \* 5 + 3

* Les opérateurs binaires demandé sont +,\*, -. 

* Toutefois on ne multiplie pas les dés entre eux. D6 \* D10 n'a pas de sens.
Quand on écrit 5 \* D6, cela signifie juste qu'on lance 5 dés à 6 faces.

* FrozenDice est utilisé pour les valeurs constantes dans un pool de dés. Ex : D10 + 5.

* Quand on multiplie un dés par un entier c'est pour faire l'équivalent de la notation nDx des jeux de rôles, et ce, quelque soit le sens. 
Par exemple : 2 \* D6()+6 s'affiche via repr par « 2D6 + 6 ».
Ainsi D6() \* 2 + 6, s'affichera de la même manière.

* nDx en jeux de rôle signifie "lance n dés à x face", on ne multiplie pas la valeur d'un dés mais on lance plusieurs dés.

* On ne 'show' qu'un Pool de dés qui a été lancé (throw). Chaque dés est lancé séquentiellement de manière pseudo-aléatoire. La méthode show retourne la séquence des dés lancés sous forme de chaîne de caractère séparés par une virgule (comme dans l'exemple précédé par un espace).

* AbstractResult.seed permet de contrôler l'aléat généré par les fonctions random. Pour une seed X connu, les jets de dés seront identique entre 2 run du module (comportement standard des fonctions aléatoires).

Success 
------- 
Codez la méthode `def success(self, lamb) → float` dans la classe Pool de tel manière que l'on puisse calculer la probabilité de chance qu'un throw soit un succès. La lambda lamb définit ce qu'on entends par succès. La lambda reçoit en unique paramètre un tuple représentant un jet de dés (chaque élément du tuple donne la valeur de chaque dés). La lambda sera évidement appelé par success pour toutes les solutions possibles pour ce jet de dés.
Par exemple, dans le RPG "Star Wars" un succès c'est quand avec la somme d'un certain nombre de D6 ont dépasse un seuil. 6D6 étant une valeur de compétence correct, et un niveau de difficulté de 30 un acte héroïque...

```python

    proba = (D6() * 6).success(lambda x: sum(x) >= 30)
    print("=> check %s%%" % proba)
```

```shell
    => check 1.9675925925925926%
```

> Avec 2 % de chance de réussir on comprend mieux l’héroïsme.

Lambda 
------
Dans le système "World Of Darkness", on compte le nombre de fois qu'un D10 dépasse (dans une poignée de dés) une certaine valeur par dés. Si le nombre de dés ainsi calculé dépasses un certain objectif c'est un succès.
Vous devez donc fournir une lambda stocké dans une variable de la classe __Pool__ et nommé __darkness__ qui compte le nombre de dés ≥ 5 et si le nombre total de dés remplissant ce contrat est ≥ 4 alors c'est un succès.

```python

    import jdr
    proba = (jdr.D10() * 5).success(jdr.Pool.darkness)
    print("=> check %s%%" % proba)
```

```shell

    => check 33.696%

```

> **module autorisés: itertools et tous les modules standards**
