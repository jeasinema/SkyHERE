# -*- coding: UTF-8 -*-
import cv2
import numpy as np
import sys

#mtx = np.load('mtx.npy')
#dist = np.load('dist.npy')
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

while(True):
    frame = cv2.imread("34.png")
    frame_cvt = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # resize的坐标是正的
    mask = cv2.inRange(frame_cvt, np.array([60, 80, 120]), np.array([100, 125, 150]))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    mask_origin = mask
    #轮廓查找
    a, contours, c = cv2.findContours(mask, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours[1]
    #print len(contours)
    #if cv2.isContourConvex(cnt):
    x,y,w,h = cv2.boxPoints(cv2.minAreaRect(cnt))
    #x,y,w,h = cv2.boundingRect(cnt)
    #mask = cv2.rectangle(mask,(tuple)(x),(tuple)(y),(255,255,255),2)
    #print x,y,w,h
    cv2.line(mask, (tuple)(x),(tuple)(y),(255,255,255),2)
    cv2.line(mask, (tuple)(y),(tuple)(w),(255,255,255),2)
    cv2.line(mask, (tuple)(w),(tuple)(h),(255,255,255),2)      
    cv2.line(mask, (tuple)(h),(tuple)(x),(255,255,255),2)

    rows, cols = mask.shape[:2]
    [vx,vy,x,y] = cv2.fitLine(cnt, cv2.DIST_L2,0,0.01,0.01)
    lefty = int((-x*vy/vx) + y)
    righty = int(((cols-x)*vy/vx)+y)
    mask = cv2.line(mask,(cols-1,righty),(0,lefty),(255,255,255),2)
    cv2.putText(mask, (str)(np.arctan((lefty-righty)/(1-cols))/3.1415926*180), (400,300), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255))

    #cv2.drawContours(mask, contours, 1, (255, 0, 0), 1)
    #v_evl = cv2.resize(frame, (64, 48))
    #count = 0
    #for i in range(1, 48):
    #    for j in range(1, 64):
    #        count = count + v_evl[i, j, 2]
    #count = count / (48 * 64)
    
    
    #if flag == 'HSV':
    #    frame_cvt = cv2.cvtColor(cv2.undistort(cap.read()[1], mtx, dist), cv2.COLOR_BGR2HSV)
    #else:
    #    frame_cvt = frame
    cv2.circle(frame, (color[0], color[1]), 10, (255, 0, 0), 0)
    cv2.putText(frame,flag + (str)(color) + (str)(frame_cvt[color[1], color[0], :]),(color[0], color[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5 ,(255, 0, 0))
    cv2.imshow('image', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('mask_origin', mask_origin)
    cv2.waitKey(0)

