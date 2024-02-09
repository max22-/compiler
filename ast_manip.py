from zipper import Zipper, ZipperError
from nodes import *
from code_generator import builtins

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
        return True
    
def lift_quotations(ast):
    counter = 0
    quotations = []
    z = make_zipper(ast)
    z.post_order_next(start=True)
    while not z.is_root():
        n = z.node()
        if isinstance(n, Quotation):
            name = f'quotation{counter}'
            quotations.append(Definition([Word(name)] + n.children()))
            z.edit(lambda n: LiftedQuotation(name))
            counter += 1
        z.post_order_next()
    z.top()
    for q in quotations:
        z.append_child(q)

# TODO: use 'down' instead of post_order
def move_definitions_at_end(ast):
    z = make_zipper(ast)
    definitions = []
    main = []
    z.down()
    try:
        while True:
            n = z.node()
            if isinstance(n, Definition):
                definitions.append(n)
            else:
                main.append(n)
            z.remove().top().down()
    except ZipperError:
        pass
    z.top()
    z.append_child(Main(main))
    for d in definitions:
        z.append_child(d)

# TODO: use 'down' instead of post_order
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
    definitions = definitions_list(ast)
    z = make_zipper(ast)
    z.post_order_next(True)
    while not z.is_root():
        n = z.node()
        if isinstance(n, Word):
            name = n.val
            if (not name in definitions) and (not name in builtins.keys()):
                raise ASTError(f"'{n.val}' undefined")
        z.post_order_next()


def process(ast):
    check_duplicates(ast)
    lift_quotations(ast)
    move_definitions_at_end(ast)
    check_undefined_words(ast)
    # TODO: removed unused definitions
    return ast
