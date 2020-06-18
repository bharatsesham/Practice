#!/usr/bin/env python3

import sys
import re

def purify(line):
    k = re.sub('[°-°|\:,;!@#$%^&*()""''0123456789-_`“†✠.•”’—{}]-\'', '', line)
    return k


for line in sys.stdin:
	line = line.strip()
	line = line.split(" ")
	words = [w for w in line if w.isalpha()]
	for word in words:
		print('%s\t%s' % (word, 1))

