from nodes import *

class CompileError(Exception):
    pass

print_short = "print-short-decimal"
dup = "DUP2"
swap = "SWP2"
equal = "EQU2 #00 SWP"
drop = "POP2"
add = "ADD2"
sub = "SUB2"
mul = "MUL2"
ifte = "ROT2 NIP #05 JCN ( false: ) NIP2 JSR2 #02 JMP ( true: ) POP2 ( call quotation: ) JSR2"

builtins = {
    "print-short": print_short,
    "dup": dup,
    "swap": swap,
    "=": equal,
    "drop": drop,
    "+": add,
    "-": sub,
    "*": mul,
    "ifte": ifte
}


def flatten(l):
    res= []
    for e in l:
        if isinstance(e, list):
            res.extend(flatten(e))
        else:
            res.append(e)
    return res

def compile(n):
    if isinstance(n, Integer):
        return f"#{n.val:0{4}x}"
    elif isinstance(n, Word):
        if n.val in builtins.keys():
            return builtins[n.val]
        else:
            return n.val
    elif isinstance(n, LiftedQuotation):
        return ';' + n.val
    elif isinstance(n, Definition):
        name = n.children()[0]
        body = n.children()[1:]
        return [f"@{name}", [compile(c) for c in body], "JMP2r"]
    elif isinstance(n, Main):
        return ['|0100'] + [compile(c) for c in n.children()] + ["BRK"]
    elif isinstance(n, Source):
        return '\n'.join(flatten([compile(c) for c in n.children()]))
    else:
        raise CompileError(f'unexpected node type: {type(n)}')
