from regex_sfn.context import Context
from regex_sfn.lexer import Token
from regex_sfn.nfa_fragment import Character
from regex_sfn.nfa_fragment import Concat
from regex_sfn.nfa_fragment import Star
from regex_sfn.nfa_fragment import Union

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.look = None
        self.move()

    def match(self, tag):
        if self.look.kind != tag:
            raise Exception("syntax error")
        self.move()

    def move(self):
        self.look = self.lexer.scan()

    def factor(self):
        if self.look.kind == Token.LPAREN:
            self.match(Token.LPAREN)
            node = self.subexpr()
            self.match(Token.RPAREN)
            return node
        else:
            node = Character(self.look.value)
            self.match(Token.CHARACTER)
            return node

    def star(self):
        node = self.factor()
        if self.look.kind == Token.OPE_STAR:
            self.match(Token.OPE_STAR)
            node = Star(node)
        return node

    def subseq(self):
        node1 = self.star()
        if self.look.kind == Token.LPAREN\
            or self.look.kind == Token.CHARACTER:
            node2 = self.subseq()
            node = Concat(node1, node2)
            return node
        else:
            return node1

    def seq(self):
        if self.look.kind == Token.LPAREN\
            or self.look.kind == Token.CHARACTER:
            return self.subseq()
        else:
            return Character("")

    def subexpr(self):
        node = self.seq()
        if self.look.kind == Token.OPE_UNION:
            self.match(Token.OPE_UNION)
            node2 = self.subexpr()
            node = Union(node, node2)
        return node

    def expression(self):
        node = self.subexpr()
        self.match(Token.EOF)

        context = Context()
        fragment = node.assemble(context)
        return fragment.build()
