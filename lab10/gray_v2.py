#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import cv2
import sys

img_name = sys.argv[1]

img = cv2.imread(img_name)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
plt.hist(gray.ravel(), bins = 256, density = 1)
plt.xlabel("gray level")
plt.ylabel("value")
plt.title("gray level of %s" %img_name)
plt.show()
