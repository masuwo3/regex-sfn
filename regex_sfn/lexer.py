class Lexer:
    def __init__(self, string_):
        self.string_list = list(string_)

    def scan(self):
        if not self.string_list:
            return Token(None, Token.EOF)

        ch = self.string_list.pop(0)

        if ch == '\\':
            return Token(self.string_list.pop(0), Token.CHARACTER)
        elif ch == '|':
            return Token(ch, Token.OPE_UNION)
        elif ch == '(':
            return Token(ch, Token.LPAREN)
        elif ch == ')':
            return Token(ch, Token.RPAREN)
        elif ch == '*':
            return Token(ch, Token.OPE_STAR)
        else:
            return Token(ch, Token.CHARACTER)

class Token:
    CHARACTER = 0
    OPE_UNION = 1
    OPE_STAR = 2
    LPAREN = 3
    RPAREN = 4
    EOF = 5

    def __init__(self, value, kind):
        self.value = value
        self.kind = kind
