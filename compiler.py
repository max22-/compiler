#!/usr/bin/env python3

import sys
import tal
from parse import parse
from ast_manip import process
from code_generator import compile

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
    #print(ast)
    #print("output:")
    #print(compile(ast))

    with open(tal_path, 'w') as f:
        f.write(tal.header)
        f.write(compile(ast))
        f.write('\n')
        f.write(tal.print_short)