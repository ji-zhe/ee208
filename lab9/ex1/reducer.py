#!/usr/bin/env python

import sys

current_letter = None
current_sum = 0
current_count = 0

for line in sys.stdin:
	line = line.strip()
	letter, length = line.split('\t', 1)
	try:
		length = int(length)
	except ValueError:
		continue

	if current_letter == letter:
		current_sum += length
		current_count += 1
	else:
		if current_letter:
			print '%s\t%s' % (current_letter, float(current_sum)/current_count)
		current_letter = letter
		current_count = 1
		current_sum = length

if current_letter == letter:
	print '%s\t%s' % (current_letter, float(current_sum)/current_count)


