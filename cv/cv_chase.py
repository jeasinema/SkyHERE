# -*- coding: UTF-8 -*-
import cv2
import numpy as np
import time
import sys
import serial

car = serial.Serial("/dev/tty",9600)
cap = cv2.VideoCapture(1)
color = [0, 0]
flag = True
flag1 = True
count = 0
mark = 0

speed = 0
angle = 0
max_val = 80

#TODO:

#1.提高速度，目前增加抓取后速度太慢
#2.矫正畸变
#(1)显示图片：频率约为10Hz
#(2)增加矫正，不显示图片：频率约为14Hz
#(3)不作任何处理：频率约为16Hz
#3.改至HSV色系处理
mtx = np.load('mtx.npy')
dist = np.load('dist.npy')
def car_run(speed,angle):
    global car
    global max_val
    if (speed > max_val):
        speed = max_val
    if (speed < -max_val):
        speed = -max_val
    car.write("#"+(str)(speed)+"-"+(str)(angle)+"*")
    print ("#"+(str)((int)(speed))+"-"+(str)((int)(angle))+"*")
    


def select_point(event,x,y,flags,param): 
    #local variable as default, so we should add the global tag
    global flag
    global color 
    global frame
    color = [x,y]
    if (event == cv2.EVENT_LBUTTONDOWN) and (flag):
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
mask = np.zeros([640, 480, 1], np.uint8)
while(True):
    try:
        ret, a = cap.read()
        if ret != 1:
            raise IOError
    except IOError:
        continue
    a = cv2.undistort(a, mtx, dist)
    cv2.circle(a, (color[0], color[1]), 10, (255, 0, 0), 0)
    a_hsv = cv2.cvtColor(a, cv2.COLOR_BGR2HSV)
    cv2.putText(a,'HSV' + (str)(color) + (str)(a_hsv[color[1], color[0], :]),(color[0], color[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5 ,(255, 0, 0))

    #a = cv2.imread('mvtest2.png')
    #cv2.imshow('test', a)
    #cv2.waitKey(-1)
    #for i in range(1, 3):
    #Attention! cannot use numpy.resize!!
    
    # 转换到 HSV 
    c = cv2.resize(a, (80,60))
    c = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)
    
    
    #TODO:
    #采用高斯模糊后掩膜出现带状干扰图形,检查下原因
    #c = cv2.GaussianBlur(c, (5, 5), 0, 0)



    # 设定颜色的阈值(Method1: HSV空间的绿色，与选择区域无关) 
    lower_green = np.array([40, 50, 50])   #滤除暗色区域
    upper_green = np.array([80, 255, 255])
    #实验结果:
    #       1.亮度较大的区域（V值较大）表现为色调上升，从而导致掩膜构建失效，建议初步利用V值动态调节H的阈值
    #       2.SVM？
    #       3.先做模糊处理,然后动态阈值

    #Method2: 根据鼠标点选的区域选择颜色

    # 根据阈值构建掩膜
    
    mask = cv2.inRange(c, lower_green , upper_green)
    c = np.float32(c)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, (21,21))
    #TODO:20160229
    #想办法解决tag离开视野后杂色干扰的问题



    #cv2.circle(mask, (color[0], color[1]), 10, (0, 0, 255), 1)
    ## 对原图像和掩模进行位运算 
    #res = cv2.bitwise_and(a, a, mask=mask)
    ## 显示图像 
    #cv2.imshow('res',res) 
    #k=cv2.waitKey(5)&0xFF
    #if k==27:
    #    break
    ## 关闭窗口 
    #cv2.destroyAllWindows()
    
    ret = cv2.moments(mask)
    if ret['m00'] != 0:
        x= (int)((float)(ret['m10'])/(float)(ret['m00']))
        y= (int)((float)(ret['m01'])/(float)(ret['m00']))
    else:
        x = y = 0
    
    #print  time.clock(), [x, y]
    #print [x*8,y*8]
    

    x = x * 8
    y = y * 8
    #output control data
    length = np.linalg.norm([x-320,y-240])
    if (length < 80):
        speed = 0
        angle = 0
    else:
        speed = length / 3;
        if x == 320:
            if y > 240:
                angle = 180
            else:
                angle = 0
        elif y == 240:
            if x > 320:
                angle = 90
            else:
                angle = -90
        else:        
            angle = np.arctan(((float)(x)-320)/(240-(float)(y)))
            angle = (float)(angle) / 3.1415926 * 180
            if (y > 240):
                if (x > 320):
                    angle = 180 + angle
                else:
                    angle = -180 + angle

    print angle,length, x, y
    #car_run(speed , angle)

    #car.write("#"+(str)(speed)+"-"+(str)(angle)+"*")l


        #if x < 624 and y < 464:
        #    cv2.circle(a, ((int)(x*8), (int)(y*8)), 50, (255, 0, 0), 0)
    cv2.imshow('mask', mask)
        #mark = mark + 1
        #cv2.imwrite("save/"+(str)(mark)+'.png', mask)
        #cv2.imshow('image', a)
    cv2.waitKey(1)
    #print time.clock()
    if cv2.waitKey(10) & 0xFF == ord('o'):
        flag1 = False
        print "+++++++++"
        cv2.destroyWindow('image')
    #if flag1:
    #   cv2.imwrite('./saved2/'+(str)(count)+'.png', a) 
    #   count = count + 1
    #   print time.clock()
