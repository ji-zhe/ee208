#!/usr/bin/env python
import cv2
import sys
img_name = sys.argv[1]

img = cv2.imread(img_name, cv2.IMREAD_COLOR)
size = img.shape
red = green = blue = 0
for i in range(size[0]):
    for j in range(size[1]):
        red += img[i,j,2]
        green += img[i,j,1]
        blue += img[i,j,0]
sum = red + green + blue
print 'BGR: %f\t%f\t%f' % (float(blue)/sum, float(green)/sum, float(red)/sum)
