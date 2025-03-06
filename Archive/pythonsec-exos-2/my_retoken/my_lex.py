LEXEMES = r"""(?umx)
(?P<comments>(?://[^\n]*\n{0,1}$|(?:/\*)[\s\S]*(?:\*/)))|


(?P<keywords>\b(?:auto|double|int|struct|break|else|long|switch|case|enum
|register|typedef|char|extern|return|union|const|float|short|unsigned
|continue|for|signed|void|default|goto|sizeof|volatile|if)\b)|


(?P<constants>(?:(?:0[xX]|[xX])(?:\d|[abcdefABCDEF])+[uUlL]{0,2}|(?:0[bB])[01]+$
|\d+\.{0,1}\d*[eE][\+-]{1}\d+|\.\d+[eE][\+-]{1}\d+|\d+\.{0,1}\d*[fFiIjJlL]{0,1}[uUlL]{0,2}
|\.\d+[fFiIjJlL]{0,1}[uUlL]{0,2}|'(?!\s*=)([^\\]|\\.)'))|




(?P<operators>(?:\.\.\.|\.|->|\+=|-=|/=|\*=|--|\+\+|\+|-|~|!=
|\|=|%|<<=|>>=|<<|>>|<=|>=|==|<|>|&&|&|\^|\|\||\||\?))|


(?P<identifiers>[_a-zA-Z]+[a-zA-Z0-9_]*)|



(?P<symbols>(?:[\[\](){},:;\#]|(?:(?:\*(?! =))|(?:=(?! =)))))|



(?P<strings>\".*\")|



(?P<spaces>\s+)"""
