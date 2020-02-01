#!/usr/bin/env python

import sys

for line in sys.stdin:
	line = line.strip()
	words = line.split()
	for word in words:
		if(word[0].isalpha()):
			print '%s\t%s' % (word[0].lower(), len(word))

