#!/usr/bin/env python3

import sys
import tal
from parse import parse
from ast_manip import process, lift_quotations, move_definitions_at_end, check_undefined_words

def usage():
    print(f"usage: {sys.argv[0]} program.txt output.tal")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        usage()
        exit(1)
    
    src_path = sys.argv[1]
    tal_path = sys.argv[2]

    with open(src_path, 'r') as f:
        source = f.read()

    ast = parse(source)
    process(ast)
    lift_quotations(ast)
    print(f"quotations lifted: {ast}")
    move_definitions_at_end(ast)
    print(f"definitions moved at the end: {ast}")
    check_undefined_words(ast)
    print(ast)

    with open(tal_path, 'w') as f:
        f.write(tal.header)
        f.write('|0100 LIT "H #18 DEO BRK')