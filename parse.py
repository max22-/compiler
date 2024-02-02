def lex(src):
    return [i for i in src.replace('[', ' [ ').replace(']', ' ] ').split() if i != '']

class Node:
    def __init__(self, type, val):
        self.type = type
        self.val = val

class Container(Node):
    def append(self, val):
        self.val.append(val)

class Program(Container):
    def __init__(self):
        super().__init__('program', [])
    def __repr__(self):
        return f"PROGRAM{self.val}"

class Quotation(Container):
    def __init__(self):
        super().__init__('quotation', [])

    def __repr__(self):
        return f"Q{str(self.val)}"

class Definition(Container):
    def __init__(self):
        super().__init__('definition', [])
        self.name = None
        self.wait_for_double_equal = False

    def append(self, val):
        if self.name == None:
            if not isinstance(val, Word):
                raise ParseError('expected word for definition name')
            self.name = val.val
            self.wait_for_double_equal = True
        elif self.wait_for_double_equal:
            if val != Word('=='):
                print(val)
                raise ParseError("Expected '=='")
            self.wait_for_double_equal = False
        else:
            super().append(val)

    def __repr__(self):
        return f"DEF{{name={self.name}}}{str(self.val)}"

class Atom(Node):
    def __repr__(self):
        return str(self.val)
    
    def __eq__(self, other):
        if not isinstance(other, Atom):
            return False
        return self.val == other.val

class Integer(Atom):
    def __init__(self, val):
        super().__init__('integer', val)
    
class Word(Atom):
    def __init__(self, val):
        super().__init__('word', val)

class ParseError(Exception):
    pass

def parse(src):
    tokens = lex(src)
    stack = [Program()]
    for t in tokens:
        if t == 'DEF':
            if len(stack) != 1:
                raise ParseError('Definitions must be at top level')
            stack.append(Definition())
        elif t == '.':
            if stack[-1].type != 'definition':
                raise ParseError("Unexpected '.'")
            d = stack.pop()
            stack[-1].append(d)
        elif t == '[':
            stack.append(Quotation())
        elif t == ']':
            if stack[-1].type != 'quotation':
                raise ParseError("Unexpected ']'")
            q = stack.pop()
            stack[-1].append(q)
        else:
            try:
                i = int(t)
                stack[-1].append(Integer(i))
            except ValueError:
                stack[-1].append(Word(t))
    if len(stack) > 1:
        types = reversed([n.type for n in stack[1:]])
        for t in types:
            if t == 'definition':
                raise ParseError('Non terminated definition')
            elif t == 'quotation':
                raise ParseError('Non closed quotation')
        raise ParseError('Unexpected error')
    else:
        res = stack[0]
        check(res)
        return res
            
def check(ast):
    definitions = [n.name for n in ast.val if n.type == 'definition']
    if len(definitions) != len(set(definitions)):
        raise ParseError('Duplicate function names')