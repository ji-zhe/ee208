#!/usr/bin/env python
import sys
value = None
for line in sys.stdin:
	line = line.strip()
	if not line:
		continue
	item = line.split()
	print '%s\t%s' % ( item[0], 0.0)
	value = float(item[1])/(len(item)-2)
	for c in item[2:]:
		print '%s\t%s' % (c, value)
	print '%s\t%s' % (item[0], '@ '+' '.join(item[2:]))
