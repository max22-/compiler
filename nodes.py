from zipper import Zipper

class Program:
    pass

class Atom(Program):
    def __init__(self, val):
        self.val = val

class Word(Atom):
    def __str__(self):
        return self.val
    
class LiftedQuotation(Atom):
    def __str__(self):
        return self.val

class Integer(Atom):
    def __str__(self):
        return str(self.val)

class Composite(Program):
    def __init__(self, children):
        self._children = children

    def children(self):
        return self._children
    
    def set_children(self, children):
        self._children = children
        return self
    
    def __str__(self):
        return f"[{', '.join([str(c) for c in self._children])}]"
    
class Definition(Composite):
    def __str__(self):
        return 'D' + super().__str__()

class Quotation(Composite):
    def __str__(self):
        return 'Q' + super().__str__()
    
class Main(Composite):
    def __str__(self):
        return 'M' + super().__str__()

class Source(Composite):
    def __str__(self):
        return 'S' + super().__str__()

def make_zipper(root):
    def z_is_branch(n):
        return issubclass(type(n), Composite)
    def z_children(n):
        return n.children()
    def z_make_node(n, c):
        return n.set_children(c)
    return Zipper(z_is_branch, z_children, z_make_node, root)