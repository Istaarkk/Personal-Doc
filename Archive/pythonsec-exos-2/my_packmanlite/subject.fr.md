À la racine du repository, dans le répertoire `my_packmanlite`.

Fichiers à rendre :

```
 .
 └── my_packmanlite.py
```

---

Le python nous permet de jouer avec les structures binaires avec le module **struct** et notamment les familles de fonctions pack et unpack.

C'est sympa le binaire, on peut lire des paquets réseaux en python, générer des images etc...

Pour faire simple :

- **pack**/**pack_into** permet de prendre des variables pythons et de les concaténer sous forme de buffer binaire.
- **unpack**/**unpack_from** permet de découper un buffer binaire sous forme de tuple python.

Les buffers binaires s'écrivent littéralement ainsi :

    buf = b'\xCA\xFE\xBA\xBE'

La syntaxe '\\x' permet d'écrire la valeur des octets en hexadécimale dans une chaine d'octet (**bytes**) préfixé par b.

Toutefois, il existe 2 types pour manipuler de tel buffer : 

* **bytes** pour les immutables (constante non modifiable).
* **bytearray** pour les mutables (variable classique).

Les fonctions sont à écrire dans un module "my_packman.py".

1 - ushort\_uint
----------------
Implémentez la fonction **ushort\_uint** qui prend un buffer et extrait un entier court non signé en big-endian, suivi d'un entier 32 bit non signé en big-endian.

    $ python3 -q
        import my_packman
        my_packman.ushort_uint(b'\x01\x42\x00\x01\x02\x03\xde\xad')
        >>> (322, 66051)

2 - buf2latin
-------------
Implémentez la fonction  **buf2latin** qui prend un buffer et en extrait la taille de la chaîne de caractères iso latin 1 et la chaîne qui suit.

    $ python3 -q
        import my_packman
        my_packman.buf2latin(b'\x00\x04G\xE9g\xe9zzz')
        >>> (4, 'Gégé')

3 - ascii2buf
-------------
Implémentez la fonction **ascii2buf** qui prend un nombre variable de chaîne de caractères en paramètre et les transforme en un buffer tel que :

- en premier nous avons le nombre d'éléments total dans le buffer (entier non signé 32 bit).
- ensuite chaque chaîne est concaténée et est préfixée par sa taille (entier non signé 16 bit)

    $ python3 -q
        import my_packman
        my_packman.ascii2buf("I", "like", "the", "game")
        >>> bytearray(b'\x00\x00\x00\x04\x00\x01I\x00\x04like\x00\x03the\x00\x04game')


> **module autorisés: struct**
