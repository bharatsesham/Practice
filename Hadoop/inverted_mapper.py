#!/usr/bin/env python3

import os
import sys
import re

line_count = {}

def purify(line):
    k = re.sub('[°-°|\:,;!@#$%^&*()""''0123456789-_`“†✠.•”’—{}]', '', line)
    return k


for line in sys.stdin:
    file_path = os.environ["map_input_file"]
    file_name = re.findall(r'\w+', file_path)[-2]
    line = line.strip()
    k = purify(line)
    for word in k.split(' '):
        if word not in line_count:
            line_count[word] = []
            line_count[word].append(1)
            line_count[word].append([file_name])
        else:
            line_count[word][0]+=1
            line_count[word][1].append(file_name)


for key in sorted(line_count.keys()):
    line_count[key].append(key)
    print(line_count[key])



