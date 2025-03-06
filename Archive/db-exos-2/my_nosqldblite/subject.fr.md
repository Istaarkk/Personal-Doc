À la racine du repository, dans le répertoire `my_nosqldblite`.

Fichiers à rendre :

```
 .
 └── my_civ.py

```

---

Le sujet traite de la programmation d'un jeu de stratégie au tour par tour de type civilisation.
Après avoir installé mongodb et vous être assuré que le service mongodb est bien lancé vous vous 
connecterez sur la base `mycivilisation` en local comme le montre la fonction `get_database` fournie par le module `model.py`.

1 - init_once
-------------
Implémentez la fonction python

```python

    def init_once(db, collection_name, datalist):

```

Qui charge les data de `datalist` dans la collection `collection_name` de la database `db` 
uniquement si celles-ci n'ont pas déjà été insérées.

On pourra tester ce code par le test suivant:

```python

    from model import *
    from my_civ import *
    db = get_database()
    init_once(db, "users", get_user_data())
    init_once(db, "users", get_user_data())
```

Et il n'y aura pas de doublon.

2 - get_city_by_owner
---------------------
Implémentez la fonction python

```python

    def get_city_by_owner(db, login):
```

Qui retourne la ville détenue par le login, tel que:

```python

    from model import *
    from my_civ import *

    city = get_city_by_owner(get_database(), "iopi")
    print(f"la ville {city['name']} a pour id {city['_id']} est détenu par l'ID {city['owner']}")
```

Pour vos tests, vous aurez surement à préinitialiser la base des villes via la fonction `set_all_initial_city`.
C'est ainsi que fonctionnera le correcteur initialisant préalablement un objet Random avec un seed pour le paramètre `rd` de cette fonction.

```python

    import random as rd
    import model

    rand = rd.Random(2600)
    model.set_all_initial_city(db, rand)

```


3 - add_food_into_city
----------------------
Implémentez la fonction python

```python

    def add_food_into_city(collection, city_id, apple_current, apple_by_turn, next_increase):
```

Qui rajoute à la ville `city_id` dans `collection` des champs supplémentaires pour comptabiliser 
la quantité de nourriture produite par tour. Tel que:

```python

    from model import *
    from my_civ import *

    db = get_database()
    city = get_city_by_owner(db, "hckz")
    add_food_into_city(db["mycity"], city["_id"], 25, 5, 100)
    assert city["foods"]["apple_current"] == 25
    assert city["foods"]["apple_by_turn"] == 5
    assert city["foods"]["next_increase"] == 100
```

Il ne peut y avoir qu'une seule production de nourriture pour la `city_id`, ainsi un deuxième appel 
à `add_food_into_city` pour la même ville modifiera les valeurs correspondantes.

4 - add_production_in_queue
---------------------------

Dans le contexte où vous aurez préalablement chargé la collection `buildings`.

```python
    import model
    import my_civ

    my_civ.init_once(db, "buildings", model.building_list)
```

Implémentez la fonction python

```python
    def add_production_in_queue(db, cityid, prod_name, hammer_current, hammer_by_turn):
```

Qui rajoute une construction dans la queue de construction de la ville:

- Si la ville n'avait pas précédemment de queue de production la rajoute comme étant un nouveau 
  champs `productions` de type tableau.
- Ajoute la production `prod_name` avec pour nombre de marteau courant, gagné par tour et total 
  (pour achever la production `hammer_total`) les valeurs respectives `hammer_current`, `hammer_by_turn` sont données à l'appel, le total `hammer_total` provient de la collection `buildings`.
- Il ne peut y avoir qu'une seul production pour la bi-clef `city_id, prod_name`, ainsi un deuxième appel à `add_production_in_queue` pour la même ville et la même production modifiera les valeurs de production en marteau.

