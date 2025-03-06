À la racine du repository, dans le répertoire **my_dumbsite**.

Fichiers à rendre :

```
.
├── main.py
├── model
│   └── *
└── templates
    └── *

```

---

modules non standard autorisés :

- pip3 install Flask
- pip3 install SQLAlchemy
- pip3 install flask-WTF

**modules standard autorisés : tous**

Faire un script/module "main.py" exécutable (+x) qui instancie une application Flask sur le port localhost:5000 (comportement par défaut).

URLs :

* /:    page par défaut. Affiche les autres liens (ne sera pas testé).

* /add\_user:   Affiche un formulaire (Flask.wtf), avec les champs suivants (on précise ici les attributs 'id' html):

    - name      pour stocker un prénom
    - lastname  pour stocker un nom
    - login     pour stocker un login
    - desc      pour stocker un texte

```html
        exemple:
        <input type=text id=name />
```

Le formulaire stocke dans une BDD via SQLAlchemy/sqlite. Vous devez créer le model et vous devez créer une base vide si votre fichier '.db' n'est pas présent dans le répertoire *model*.

* /list\_user:  Affiche une liste de liens avec pour valeur affichée le login vers la page /show_user en contenant l'id en base de donnée.

* /show\_user/01234...56789:  Cette page affiche sous forme de fiche le contenu en BDD pour l'id donnée.
        Chaque champ est affiché dans une balise `div` avec un attribut `class` correspondant au formulaire (name, lastname, login, desc).

Pensez à vider vos bases des données de test avant de push !

Le répertoire **model** contiendra tout ce qui concerne la partie BDD.

Le répertoire **templates** contiendra vos templates htmls.
