#!/usr/bin/env python3
import sys
import os

filename=sys.argv[1]

if not os.path.exists(filename):
    with open(filename, "w") as f:
        f.write("New File created\n")
    sys.exit(1)
else:
    print("Error, the file {} exists already".format(filename))
    sys.exit(2)
