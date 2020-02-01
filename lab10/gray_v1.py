#!/usr/bin/env python
import cv2
import sys

img_name = sys.argv[1]

img = cv2.imread(img_name)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
container = [0]*256
for line in gray:
    for i in line:
        container[i] += 1
s = sum(container)
for i in container:
    print '%f\t' % (float(i)/s),
