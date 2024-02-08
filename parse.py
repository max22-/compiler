from nodes import *
from zipper import Zipper

def lex(src):
    return [i for i in src.replace('[', ' [ ').replace(']', ' ] ').split() if i != '']

class ParseError(Exception):
    pass

def parse(src):
    tokens = lex(src)
    z = make_zipper(Source([]))
    for t in tokens:
        if t == 'DEF':
            if not isinstance(z.node(), Source):
                raise ParseError('Definitions must be at top level')
            z.append_child(Definition([]))
            z.down().rightmost()
        elif t == '.':
            if not isinstance(z.node(), Definition):
                raise ParseError("unexpected '.'")
            z.up()
        elif t == '[':
            z.append_child(Quotation([]))
            z.down().rightmost()
        elif t == ']':
            if not isinstance(z.node(), Quotation):
                raise ParseError("Unexpected ']'")
            z.up()
        else:
            try:
                i = int(t)
                z.append_child(Integer(i))
            except ValueError:
                z.append_child(Word(t))
    res = z.node()
    if not isinstance(res, Source):
        raise ParseError(f"unterminated {type(res)}")
    return res