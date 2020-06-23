#!/usr/bin/env python3
import sys
import math
import time

train = []
test = []


for lines in sys.stdin:
	lines = lines.strip()
	features = [float(x) for x in lines.split(',')]
	if features[-1]!=-1.0:
		train.append(features)
		continue
	else:
		test.append(features[:-1])

for test_value, values in enumerate(test):
	streaming_data = []
	for features, lines in enumerate(train):
		avg = 0.0
		data = []
		data.extend(values)
		for i in range(len(lines)-1):
			avg += (float(lines[i]) - float(values[i]))**2
		dist = math.sqrt(avg)
		data.append(str(lines[-1]))
		data.append(str(dist))
		data.append(str(test_value))
		print(data)



