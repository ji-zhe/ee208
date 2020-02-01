#!/usr/bin/env python
import cv2
import numpy as np
import sys

img_name = sys.argv[1]

img = cv2.imread(img_name)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

a, b = gray.shape
container = np.zeros((a-2,b-2))
for i in range(1, a-2):
    for j in range(1, b-2):
        container[i-1,j-1] =( (int(gray[i+1,j])-int(gray[i-1,j]))**2+(int(gray[i,j+1]) -int( gray[i,j-1]))**2)**0.5
ans = [0] * 361
for i in range(a-2):
    for j in range(b-2):
        ans[int(container[i,j])]+= 1
s = sum(ans)
for i in range(len(ans)):
    ans[i] = float(ans[i])/s
    print '%f\t' % ans[i],
