class ZipperError(Exception):
    pass

class Zipper:
    def __init__(self, is_branch, children, make_node, root):
        self._is_branch = is_branch
        self._children = children
        self._make_node = make_node
        self.focus = root
        self.path = []
    
    def is_root(self):
        return len(self.path) == 0

    def up(self):
        if len(self.path) == 0:
            raise ZipperError('Already at the top')
        crumb, self.path = self.path[0], self.path[1:]
        self.focus = self._make_node(crumb['pnode'], crumb['l'] + [self.focus] + crumb['r'])
        return self

    def down(self):
        if (not self._is_branch(self.focus)) or len(self._children(self.focus)) == 0 :
            raise ZipperError('Already at the bottom')
        children = self._children(self.focus)
        self.path = [{'pnode': self.focus, 'l': [], 'r': children[1:]}] + self.path
        self.focus = children[0]
        return self

    def left(self):
        if len(self.path) == 0:
            raise ZipperError('Left of root')
        if len(self.path[0]['l']) == 0:
            raise ZipperError('Already at leftmost node')
        l = self.path[0]['l']
        r = self.path[0]['r']
        r = [self.focus] + r
        self.focus = l.pop()
        self.path[0]['l'] = l
        self.path[0]['r'] = r
        return self
        

    def right(self):
        if len(self.path) == 0:
            raise ZipperError('Right of root')
        if len(self.path[0]['r']) == 0:
            raise ZipperError('Already at rightmost node')
        l = self.path[0]['l']
        r = self.path[0]['r']
        l.append(self.focus)
        self.focus = r[0]
        r = r[1:]
        self.path[0]['l'] = l
        self.path[0]['r'] = r
        return self

    def top(self):
        while len(self.path) > 0:
            self.up()
        return self

    def bottom(self):
        try:
            while True:
                self.down()
        except ZipperError:
            return self

    def leftmost(self):
        if len(self.path) > 0:
            while len(self.path[0]['l']) > 0:
                self.left()
        return self

    def rightmost(self):
        if len(self.path) > 0:
            while len(self.path[0]['r']) > 0:
                self.right()
        return self
    
    def post_order_next(self, start=False):
        if not start and self.is_root():
            raise ZipperError('Tree already walked')
        if start:
            return self.bottom()
        try:
            return self.right().bottom()
        except ZipperError:
            return self.up()

    def node(self):
        return self.focus
    
    def edit(self, f):
        self.focus = f(self.focus)
        return self
    
    def remove(self):
        if self.is_root():
            raise ZipperError("Remove at root")
        r = self.path[0]['r']
        l = self.path[0]['l']
        if len(r) > 0:
            self.focus = r[0]
            self.path[0]['r'] = r[1:]
        elif len(l) > 0:
            self.focus = l.pop()
            self.path[0]['l'] = l
            self.up()
        else:
            self.up()
            self.focus = self._make_node(self.focus, [])
        return self
    
    def append_child(self, c):
        if not self._is_branch(self.focus):
            raise ZipperError('Cannot add child to leaf node')
        children = self._children(self.focus)
        children.append(c)
        self.focus = self._make_node(self.focus, children)
        return self
    
    def __repr__(self):
        return f"({self.focus}, {self.path})"
