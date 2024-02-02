#!/usr/bin/env python3

import sys
import tal
from parse import parse

def usage():
    print(f"usage: {sys.argv[0]} program.txt output.tal")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        usage()
        exit(1)
    
    src_path = sys.argv[1]
    tal_path = sys.argv[2]

    with open(src_path, 'r') as f:
        print(parse(f.read()))

    with open(tal_path, 'w') as f:
        f.write(tal.header)
        f.write('|0100 LIT "H #18 DEO BRK')