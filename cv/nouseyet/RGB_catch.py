# -*- coding: UTF-8 -*-
import cv2
import numpy as np
import time

cap = cv2.VideoCapture(1)
color = []
flag = True
flag1 = True
count = 0

#TODO:
#1.提高速度，目前增加抓取后速度太慢
#2.矫正畸变
#(1)显示图片：频率约为10Hz
#(2)增加矫正，不显示图片：频率约为14Hz
#(3)不作任何处理：频率约为16Hz
mtx = np.load('mtx.npy')
dist = np.load('dist.npy')
def select_point(event,x,y,flags,param): 
    #local variable as default, so we should add the global tag
    global flag
    global color 
    global frame
    if (event == cv2.EVENT_LBUTTONDOWN) and (flag):
        color = [x,y]
        print color
        # 图片坐标是反的, 但是作图则是正的！
        cv2.circle(frame, (x, y), 10, (255, 0, 0), 0)
        frame = cv2.undistort(frame, mtx, dist)
        cv2.imshow('image', frame)
        print frame[y,x,:]
        flag = False
        print "click"
        cv2.waitKey(0)

cv2.namedWindow('image') 
cv2.setMouseCallback('image',select_point)
#mouse to select the target
while(flag):
    try:
        ret, frame = cap.read()
        if ret != 1:
            raise IOError
        #创建图像与窗口并将窗口与回调函数绑定 
        frame = cv2.undistort(frame, mtx, dist)
        cv2.imshow('image', frame)
        cv2.waitKey(1)
    except IOError:
        continue
#recognize the color
green = frame[color[1], color[0], :]
#green = [42,144,78]
print green
#cv2.waitKey(0)
threshold = 42 
c = np.zeros((48, 64, 3), np.float32)
while(True):
    try:
        ret, a = cap.read()
        if ret != 1:
            raise IOError
    except IOError:
        continue
    a = cv2.undistort(a, mtx, dist)
    #a = cv2.imread('mvtest2.png')
    #cv2.imshow('test', a)
    #cv2.waitKey(-1)
    #for i in range(1, 3):
        #Attention! cannot use numpy.resize!!
    c = cv2.resize(a, (64, 48))
    c = np.float32(c)
    #cv2.imshow('c', np.uint8(c))
    #cv2.waitKey(-1)
    b = np.zeros((48, 64), np.float32);
    for i in range(1, 48):
        for j in range(1, 64):
            color = c[i, j,:]
            color = np.reshape(color, (1, 3))
            diff = np.absolute(color - green)
            diff = np.linalg.norm(diff);
            if diff < threshold:
                b[i, j] = 1
   # print b
   # cv2.waitKey(0)
    ret = cv2.moments(b)
    if ret['m00'] != 0:
        x= (int)((float)(ret['m10'])/(float)(ret['m00']))
        y= (int)((float)(ret['m01'])/(float)(ret['m00']))
    else:
        x = y = 0
    print [x*8,y*8]
    if flag1:    
        if x < 664 and y < 464:
            cv2.circle(a, ((int)(x*8), (int)(y*8)), 50, (255, 0, 0), 0)
        cv2.imshow('image', b)
        cv2.waitKey(1)
    print time.clock()
    if cv2.waitKey(10) & 0xFF == ord('o'):
        flag1 = False
        print "+++++++++"
        cv2.destroyWindow('image')
    #if flag1:
    #   cv2.imwrite('./saved2/'+(str)(count)+'.png', a) 
    #   count = count + 1
    #   print time.clock()
