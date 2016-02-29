import cv2
import numpy as np

gray  = cv2.imread('moment.png') 
print gray.shape
gray = cv2.cvtColor(gray , cv2.COLOR_BGR2GRAY)
print gray
print gray.shape
#cv2.imshow('test', gray)
#cv2.waitKey(-1)
ret = cv2.moments(gray)
print ret
a= (int)((ret['m10'])/(float)(ret['m00']))
b= (int)((ret['m01'])/(float)(ret['m00']))
gray = cv2.cvtColor(gray , cv2.COLOR_GRAY2BGR)
cv2.circle(gray,(a,b), 0, (255,0,0), 0)
cv2.imshow('show',gray)
cv2.waitKey(-1)
