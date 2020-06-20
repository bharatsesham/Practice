#!/usr/bin/python3

import sys

emp_name_dict = {}
emp_detail_dict = {}

for line in sys.stdin:
    line = line.strip()
    emp_id, name, sal, cntry, pwd = line.split('\t')
    if pwd == "-1":
        emp_name_dict[emp_id] = name
    else:
        emp_detail_dict[emp_id] = [sal, cntry, pwd]


for emp_id in emp_detail_dict.keys():
    emp_id = emp_id
    name = emp_name_dict[emp_id]
    sal = emp_detail_dict[emp_id][0]
    cntry = emp_detail_dict[emp_id][1]
    pwd = emp_detail_dict[emp_id][2]

    print ('%s\t%s\t%s\t%s\t%s'% (emp_id, name, sal, cntry, pwd))



