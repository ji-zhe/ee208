#!/usr/bin/env python
import sys
values = 0.0
alpha = 0.85
N = int(sys.argv[1])
results = dict()
links = dict()

content = sys.stdin.readlines()
flag = 0
for line in content:
    if not line.strip():
        break
    data = line.strip().split()
    if '@' in data:
        links[data[0]] = data[2:]
        continue
    page,value = data[0],float(data[1])
    if page in results:
        results[page] += value
    else:
        results[page] = value
for key in results:
    print '%s\t%f\t%s' % (key, results[key]*alpha + (1-alpha)/N, ' '.join(links[key]))
