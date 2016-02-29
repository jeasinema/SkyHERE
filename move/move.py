# -*- coding: UTF-8 -*-
import sys
#import serial
import time
import cv2
import numpy as np

#if len(sys.argv) > 1:
#    sername = "/dev/ttyUSB"+(str)sys.argv[1]
#else:
#    sername = "/dev/ttyUSB0"
#car = serial.Serial(sername, 115200)

ellipse_center = (320, 480)   #绘图坐标以左上角为原点，先横后竖
line_length = 0
line_dir = 0

def control_point(event, x, y, flags, param):
    global ellipse_center
    global line_length
    global lint_dir
    cv2.line(catch, ellipse_center, (x, y), (255, 0 , 0), 2)
    line_length = np.linalg.norm([[x ,y], [320, 480]])
    line_dir = np.arctan((ellipse_center[1] - y)/(x - ellipse_center[0])) 
    print x,y,line_length,line_dir

cv2.namedWindow('fpv')
cv2.setMouseCallback('fpv',control_point)
cap = cv2.imread("../2.png")
while(True):
    try:
        #ret, catch = cap.read()
        ret = 1
        catch = cap
        if ret == 0:
            raise IOError
        cv2.ellipse(catch, ellipse_center, (300, 80), 0, 0, 360, (255, 0, 0), 2)
        cv2.imshow('fpv',catch)
        cv2.waitKey(1)
    except IOError:
        continue


