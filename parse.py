from nodes import *
from zipper import Zipper
from collections import deque

def lex(src):
    return deque([i for i in src.replace('[', ' [ ').replace(']', ' ] ').split() if i != ''])

class ParseError(Exception):
    pass

def parse(src):
    tokens = lex(src)
    z = make_zipper(Source([]))
    while len(tokens) > 0:
        t = tokens.popleft()
        if t == 'DEF':
            if not isinstance(z.node(), Source):
                raise ParseError('Definitions must be at top level')
            z.append_child(Definition([]))
            z.down().rightmost()
            if len(tokens) == 0:
                raise ParseError('unterminated definition')
            t = tokens.popleft()
            if not t[0].isalpha():
                raise ParseError(f'Invalid definition name: {t}')
            z.append_child(Word(t))
            if len(tokens) == 0:
                raise ParseError(f"unterminated definition for '{t}'")
            t = tokens.popleft()
            if t != '==':
                raise ParseError("Expected '==' after definition name")
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