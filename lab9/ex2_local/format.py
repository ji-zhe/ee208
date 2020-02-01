#!/usr/bin/env python
import sys

links = dict()
value = dict()

for line in sys.stdin:
    line = line.strip().split()
    if '@' in line:
        links[line[0]] = line[2:]
    elif line:
        value[line[0]] = line[1]

for key in links:
    print key+'\t'+value[key]+'\t'+' '.join(links[key])
