from zipper import Zipper, ZipperError
from nodes import make_zipper, Quotation, Definition, Word

global_env = {
    "println": None,
    "dup": None,
    "=": None,
    "ifte": None,
    "drop": None,
    "-": None,
    "*": None,
}

class ASTError(Exception):
    pass

def check_duplicates(ast):
    z = make_zipper(ast)
    z.down()
    definitions = []
    try:
        while True:
            n = z.node()
            if isinstance(n, dict):
                name = n['body'][0]
                if name in definitions:
                    raise ASTError(f"Duplicate definition name: {name}")
                definitions.append(name)
            z.right()
    except ZipperError:
        print(f"definitions = {definitions}")
        return True
    
def lift_quotations(ast):
    counter = 0
    quotations = []
    z = make_zipper(ast)
    z.post_order_next(start=True)
    while not z.is_root():
        n = z.node()
        if isinstance(n, Quotation):
            name = Word(f'_quotation{counter}')
            quotations.append(Definition([name] + n.children()))
            z.edit(lambda n: name)
            counter += 1
        z.post_order_next()
    z.top()
    for q in quotations:
        z.append_child(q)

def move_definitions_at_end(ast):
    z = make_zipper(ast)
    definitions = []
    z.post_order_next(start=True)
    while not z.is_root():
        n = z.node()
        if isinstance(n, Definition):
            definitions.append(n)
            z.remove()
        else:
            z.post_order_next()
    z.top()
    for d in definitions:
        z.append_child(d)

def definitions_list(ast):
    z = make_zipper(ast)
    definitions = []
    z.post_order_next(start=True)
    while not z.is_root():
        n = z.node()
        if isinstance(n, Definition):
            definitions.append(n.children()[0].val)
        z.post_order_next()
    return definitions

def check_undefined_words(ast):
    print(f"ast: {ast}")
    definitions = definitions_list(ast)
    z = make_zipper(ast)
    print(z)
    z.post_order_next(True)
    while not z.is_root():
        n = z.node()
        if isinstance(n, Word):
            print(n)
            if (not n.val in definitions) and (not n.val in global_env.keys()):
                raise ASTError(f"'{n.val}' undefined")
        z.post_order_next()


def process(ast):
    check_duplicates(ast)
    return ast
