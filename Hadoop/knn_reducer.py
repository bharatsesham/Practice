#!/usr/bin/env python3

import sys
from operator import itemgetter
import time
import ast


distances=[]
estimateval = 0.0
k = 25


for lines in sys.stdin:
	lines=lines.strip()
	distances.append(ast.literal_eval(lines))


for test_value in set(test_data[-1] for test_data in distances):
	output = []
	distance = [x for x in distances if x[-1]==test_value]
	output.append(test_value)
	output.extend(distance[0][:-3])
	distance = sorted(distance,key=itemgetter(-2))
	pred_class = []
	for i in range(k):
		pred_class.append(distance[i][-3])
	out = int(float(max(set(pred_class), key=pred_class.count)))
	output.append(out)
	print (output)


