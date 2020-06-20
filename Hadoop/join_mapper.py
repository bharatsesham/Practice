#!/usr/bin/python3

import sys

for line in sys.stdin:
    line = line.strip()
    line = line.split(",")

    emp_id = "-1"
    sal = "-1"
    cntry = "-1"
    pwd = "-1"
    name = "-1"

    if len(line) == 4:
        emp_id = line[0]
        sal = line[1]
        cntry = line[2]
        pwd = line[3]
    else:
        emp_id = line[0]
        name = line[1]
    print('%s\t%s\t%s\t%s\t%s' % (emp_id, name, sal, cntry, pwd))
