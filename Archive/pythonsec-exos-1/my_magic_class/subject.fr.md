À la racine du repository, dans le répertoire `my_magic_class`.

Fichiers à rendre :

```
 .
 └── my_magic_class.py
```

---

Il vous est demandé de réaliser un module python nommé `my_magic_class` tel que:

```python

    import my_magic_class as m

    test = m.Dummy(a=12, b="2600")
    assert test.desc == "instance magic"
    assert test.a == 12
    assert test.b == "2600"
    
    test = m.Dummy(unicorn="pink invisible", desc="le constructeur est magic")
    assert test.desc == "le constructeur est magic"
    assert test.unicorn == "pink invisible"

    test = m.Dummy(1, 2, 3, 4, desc="non vraiment")
    assert test[0] == 1
    assert test[1] == 2
    assert test[2] == 3
    assert test[3] == 4
    assert test.desc == "non vraiment"
```

> **module autorisés: builtins**
