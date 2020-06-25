#!/usr/bin/env python3

import sys
import ast
from collections import Counter

count= {}

for line in sys.stdin:
    k = ast.literal_eval(line)
    if k[2] not in count:
        count[k[2]] = []
        count[k[2]].append(k[1])
    else:
        count[k[2]].append(k[1])

for key in sorted(count.keys()):
    print(str(key)+ " "+str(count[key]))

