#!/usr/bin/env python
import cv2
import numpy as np
import sys
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

img_name = sys.argv[1]

img = cv2.imread(img_name)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

a, b = gray.shape
container = np.zeros((a-2,b-2))
for i in range(1, a-2):
    for j in range(1, b-2):
        container[i-1,j-1] =( (int(gray[i+1,j])-int(gray[i-1,j]))**2+(int(gray[i,j+1]) -int( gray[i,j-1]))**2)**0.5
plt.hist(container.ravel(), bins=361, density = 1)
plt.xlabel("gradient")
plt.ylabel("value")
plt.title("gradient of %s" % img_name)
plt.show()
