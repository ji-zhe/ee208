#!/usr/bin/env python
import sys

for line in sys.stdin:
	line = line.strip()
	item = line.split()
	print item[0], item[1]
	print item[0], '@',
	for i in range(2, len(item)):
		print item[i],
	print ''
