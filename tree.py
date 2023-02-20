#!/usr/bin/env python

from __future__ import print_function, unicode_literals
import os
import sys

def walk_level(root_path, max_depth=3):
    for root, dirs, files in os.walk(root_path, topdown=True):
        depth = root[len(root_path) + len(os.path.sep):].count(os.path.sep)
        if int(depth) >= int(max_depth):
            del dirs[:]
        else:
            print(f"Level {depth}: {root}")
            for file in files:
                print(f" - {file}")

if __name__ == '__main__':    
    # example usage
    if len(sys.argv) == 1:
        print("usage: DIRECTORY LEVEL[default=3]")
    else:
        if len(sys.argv) == 3:
            if sys.argv[2].isdigit():
                walk_level(sys.argv[1], sys.argv[2])
        elif len(sys.argv) == 2:
            walk_level(sys.argv[1], max_depth=3)
