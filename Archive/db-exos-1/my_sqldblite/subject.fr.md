À la racine du repository, dans le répertoire `my_sqldblite`.

Fichiers à rendre :

```
└── my_request.py
```

---

Le sujet traite de la programmation d’un jeu de rôle au tour par tour jouable en
ligne via un site web et des web-services communiquant avec la base de données.

Pour cela on vous donne un fichier `model.py` par lequel vous devez charger le fichier `model.sql` et `initdata.sql`.
Dans l'exemple ci-dessous on vous donne aussi la liste des `account` par défaut.

0 - bdd:
-------

Pour vos test vous aurez à créer un script de création du fichier `model.db`. Pour faire cela votre fichier de test sera similaire à:
    
```python
    from model import *
    
    m = Model()
    m.load_sql('model.sql')
    m.insert_account([
        ('theo', 'jarmin', 'theodore', Passwd('1ow0jsc8n'), 'theo823@gmail.com'),
        ('jiji', 'hijom', 'juliette', Passwd('21#!@PL!@'), 'jul.hijom@free.fr'),
        ('hckz', 'hacheman', 'joe', Passwd('11111'), '_1234@free.fr'),
        ('iopi', 'auroux', 'lionel', Passwd('213l1i8j12[;'), 'lionel.auroux@gmail.com')
        ])
    m.load_sql('initdata.sql')
```

Ce fichier de test ne sera pas à rendre, ni le fichier `model.db`.
La correction se fera sur une BD neuve chargée comme l'exemple précédent.

Pour les détails, le fichier `model.py` vous est donné. Il contient la définission de la classe `Model`, les méthodes `load_sql` et `insert_account`, ainsi que la fonction `Passwd`.

De même, vous sont données les fichiers `model.sql` créant le schéma de la BDD et `initdata.sql` chargeant les données du jeu.

Ces 2 fichiers sont largement commentés, et sont à lire pour une meilleur compréhension des règles.

1 - v_avatar:
------------

```python

    def load_v_avatar(model):
        pass
```

Dans le module à rendre vous devez fournir la fonction `load_v_avatar` qui va créer dans le modèle une vue `v_avatar` retournant les avatars actifs pour les joueurs par login.

La fonction `load_v_avatar` ne retourne rien.

La vue `v_avatar` doit retourner les colonnes suivantes:

- acc_login
- acc_name
- acc_surname
- av_name
- av_exp
- av_level

Cette vue est le résultat d'une jointure, et est toujours présenté ordonnée par `acc_login` puis `av_name` ascendant.

2 - v_ingame:
------------

```python

    def load_v_ingame(model):
        pass
```

Dans le module à rendre vous devez fournir la fonction `load_v_ingame` qui va créer dans le modèle une vue `v_ingame` retournant tous les avatars actuellement en jeu par login descendant puis nom d'avatar descendant.

La fonction `load_v_ingame` ne retourne rien.

La vue `v_ingame` doit retourner les colonnes suivantes:

- acc_login
- av_name
- av_pos_x
- av_pos_y

av_pos_x, av_pos_y sont des colonnes obtenues par renommage des colonnes `mob_pos_x`, `mob_pos_y` des avatars en cours de jeu lors de la requête à rendre.

3 - v_race_class:
----------------

```python

    def load_v_race_class(model):
        pass

```

Fournir une fonction python `load_v_race_class` qui crée la vue `v_race_class` retournant une table de progression pour chaque combinaison de race/classe. 

La fonction `load_v_race_class` ne retourne rien.

La vue `v_race_class` doit retourner les colonnes suivantes:

- race_key_name
- race_long_name
- cls_key_name
- cls_long_name
- required_exp_by_level
- bonus_hp_by_level
- bonus_cp_by_level

Le tout ordonné par expérience requise par niveau, bonus de
hit point (HP) et bonus de point de compétence (CP) tous respectivement
descendant. Il faut tenir compte des restrictions (exemple: un barbare
haut-elf, cela n’existe pas). Les bonus de classe et de race s’additionnent.

> Vous avez un exemple de rendu de la vue dans `v_race_class.txt`.

4 - account_actif:
-----------------

```python

    def f_account_actif(model, acc_login) -> bool:
        pass

```

Fournir une fonction python `f_account_actif` retournant vrai si le compte contient un (et un seul) avatar actif ou sinon faux.

5 - f_progression:
-----------------

```python

    def f_progression(model, race, cls, lvlmin, lvlmax) -> list:
        pass
```

Fournir une fonction `f_progression` retournant la liste de la progression par niveau pour une race et une classe données entre un niveau MIN et MAX.

Les valeurs HP et CP sont arrondies à l’inférieur après application des bonus.

Les bonus s’appliquent au delà du niveau 1.

**Le résultat sera produit via une unique requête SQL, pas de procédure stockée ni d'itération côté python.**

Il est conseillé de passer par [generate_series](https://sqlite.org/series.html)

> Vous avez des exemples de rendu de la fonction dans `f_progression.txt`. 
