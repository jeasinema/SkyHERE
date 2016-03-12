import cv2
import numpy as np

a = cv2.imread("34.png")
a = cv2.cvtColor(a, cv2.COLOR_BGR2HSV)
cv2.imshow("a", a)
cv2.waitKey(0)
