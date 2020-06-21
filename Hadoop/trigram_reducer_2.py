#!/usr/bin/env python3

import sys
from operator import itemgetter
from collections import defaultdict
import ast

final_data = []

for line in sys.stdin:
	if line:
		final_data.append(ast.literal_eval(line))

sorted_fd_list = sorted(final_data,key=itemgetter(1), reverse=True)

d = defaultdict(float)

for x, y in sorted_fd_list:
    d[x] += float(y)

final_list = [(x, round(y, 2)) for x, y in d.items()]

sorted_final_list = sorted(final_list,key=itemgetter(1), reverse=True)

for k,v in sorted_final_list[0:10]:
	print(k)
	
