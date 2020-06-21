#!/usr/bin/env python3

import sys
import ast

for line in sys.stdin:
	line = ast.literal_eval(line)
	for i in line:
		print(i)

