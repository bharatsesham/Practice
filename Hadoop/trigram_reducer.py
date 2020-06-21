#!/usr/bin/env python3

import sys
import nltk
import ast
from operator import itemgetter
from collections import defaultdict, Counter

 
data = []

def process_item(line):
	b = '_'.join(line)
	return b

for line in sys.stdin:
	a = process_item(ast.literal_eval(line))
	data.append(a)

count = Counter(data)
print(count.most_common(10))

