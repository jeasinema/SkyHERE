# -*- coding: UTF-8 -*-
import cv2
import numpy as np
import sys

mtx = np.load('mtx.npy')
dist = np.load('dist.npy')
color = [0, 0]
count = 0
if (len(sys.argv) < 2):
    flag = 'HSV'
else:
    if sys.argv[1] == 'HSV':
        flag = 'HSV'
    else:
        flag = 'RGB'

def color_point(event,x,y,flags,param): 
    #local variable as default, so we should add the global tag
    global flag
    global frame
    global color
    global count
    color = [x,y]
    # 图片坐标是反的, 但是作图则是正的！
    print flag ,color, frame_cvt[y,x,:], count

cv2.namedWindow('image') 
cv2.setMouseCallback('image',color_point)

cap = cv2.VideoCapture(0)
while(True):
    frame = cv2.undistort(cap.read()[1], mtx, dist) 
    # resize的坐标是正的
    v_evl = cv2.resize(frame, (64, 48))
    count = 0
    for i in range(1, 48):
        for j in range(1, 64):
            count = count + v_evl[i, j, 2]
    count = count / (48 * 64)
    
    
    if flag == 'HSV':
        frame_cvt = cv2.cvtColor(cv2.undistort(cap.read()[1], mtx, dist), cv2.COLOR_BGR2HSV)
    else:
        frame_cvt = frame
    cv2.circle(frame, (color[0], color[1]), 10, (255, 0, 0), 0)
    cv2.putText(frame,flag + (str)(color) + (str)(frame_cvt[color[1], color[0], :]),(color[0], color[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5 ,(255, 0, 0))
    cv2.imshow('image', frame)
    cv2.waitKey(1)

