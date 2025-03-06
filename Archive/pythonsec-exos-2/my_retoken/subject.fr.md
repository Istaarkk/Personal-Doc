À la racine du repository, dans le répertoire `my_retoken`.

Fichiers à rendre :

```
 .
 └── my_lex.py
```

---

Vous devez réaliser un lexer pour le langage C comme expliqué ici: https://www.geeksforgeeks.org/cc-tokens/

Toutefois les catégories reconnus par votre Lexer sont étendues à :

- keywords
- identifiers
- constants
- strings
- symbols
- operators
- spaces
- comments

Pour vous aider, il vous est fournis le module `my_retoken.py` contenant le code de la classe Lexer.
Un fichier `TestRegex101.txt` vous est aussi fournis pour saisir l'étendue des éléments que nous attendons dans la regex. Cette liste n'est pas exhaustive.

```python

    import re
    from my_lex import LEXEMES
    
    class Lexer:
        def __init__(self):
            self.pattern = re.compile(LEXEMES)

        def get_tokens(self, content):
            # fonction interne qui retourne la seul clef
            # aillant une valeur du dictionnaire d
            def get_only_key(d):
                for k, v in d.items():
                    if v is not None:
                        return k
            # position dans le contenu
            self.pos = 0
            # position de la fin de contenu
            sz = len(content)
            # en résultat, la liste des tokens parsés
            tokens = []
            # tant qu'on arrive pas au dernier caractère
            while self.pos != sz:
                # parse le premier token valide à la position courante
                try:
                    m = self.pattern.match(content, self.pos)
                except Exception as e:
                    print(f"EXCEPTION: {e}")
                    print(f"SKIP")
                    return tokens
                # si on ne match pas, c'est qu'il y a une erreur
                if m is None:
                    raise RuntimeError(f"Failed to parse {content[self.pos:]}")
                # récupere le dictionnaire des tokens
                d = m.groupdict()
                # une seule clef à une valeur
                k = get_only_key(d)
                # la clef est le type de token
                tokens.append((k, d[k]))
                # avance de ce qui a été parsé
                self.pos += len(m.group(0))
        return tokens
```

Ce module charge et utilise `my_lex.py`. Dans `my_lex.py`, on s'attend à avoir une unique chaîne de caractère nommé ``LEXEMES`` contenant une expression rationnel identifiant les différents tokens en utilisant au maximum les mécanismes étendues des regex en mode verbose ainsi que les groupes nommés (via la syntaxe `(?P<nom_groupe>pattern)` ).
Ainsi, la méthode `get_tokens` va itérativement utiliser la regex pour identifier morceau par morceau les différents tokens et fournir une liste de `tuple` des tokens en donnant leur catégories et leur valeurs.

Ci-dessous un cas typique d'utilisation de la classe Lexer.

```python

    import my_retoken as m
    lex = m.Lexer()
    res = lex.get_tokens("int a = 12;")
    assert res == [('keywords', 'int'), ('spaces', ' '), ('identifiers', 'a'),
                    ('spaces', ' '), ('symbols', '='),
                    ('spaces', ' '), ('constants', '12'), ('symbols', ';')
                ]
```

Vous pouvez utiliser https://regex101.com/ pour vous aider à concevoir votre expression rationnel.

Pour votre expression rationnel, nous vous conseillons le mode "extended" (verbose) afin de faire une expression rationnel commentés sur plusieurs lignes, ainsi que le mode unicode et multiligne. Ce qui en utilisant les annotations étendues donne pour les catégories `spaces` et `symbols` donne le code suivant :

```python

    LEXEMES = r"""(?umx)
            # la syntaxe (? ...) permet de piloter les flags globaux de la regex.
            # en mode X (verbose), vous pouvez écrire des commentaires dans votre regex,
            # car les espaces ne sont pas interprétés comme des espaces à lire.
            # nous vous conseillons aussi le mode unicode U et multiligne M ...
            # consultez la documentation pour en saisir l'impact

            # aussi nous vous imposons l'utilisation de la capture de groupe nommé via
            # la syntaxe (?P<nom_groupe>pattern)

            # lire un token de la catégorie `symbols`
            (?P<symbols>(?:
                [\[\](){},:;\#]
                |(?:
                    (?: \* (?! = ) ) # star not followed by equal
                    | (?: = (?! = ) ) # a single equal sign
                )
            )
            # lire un token de la catégorie `spaces`
            | (?P<spaces>\s+)

            # Attention l'ordre des alternatives séparés par | a du sens
            # Faites attention à l'ajout de nouvelles alternatives pour lire
            # et reconnaitre de nouveau pattern
    """
```


Vous pouvez partir de cette base et la compléter en faisant attention à l'ordre des alternatives.

> **Ne confondez pas les `symbols` et les `operators`. Ainsi, l'opérateur d'affectation `=` est un `symbols`, alors que l'affectation incrémentale `+=` est un `operators`.**

> **Vous aurez peut-être besoin à un moment donné de faire des `lookaheads` afin de distinguer certains tokens contenant des parties communes.**
