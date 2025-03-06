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
