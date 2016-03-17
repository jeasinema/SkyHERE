#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# ----------------------------------
# File Name : mv_blurcatch_diff.py
# Purpose :
# Creation Date : 16-03-2016
# Last Modified : Wed Mar 16 23:43:54 2016
# Created By : Jeasine Ma
# ---------------------------------
import numpy as np
import cv2
from functools import wraps
from cv_interface import videoHandle as myv
from move_interface import carHandle as myc
from decos_interface import decos

#car = myc(0, 9600)
cam = myv(1)
#cam.select_image_color()
#car.send_cmd(0, 0)

#mask_pre = np.zeros((cam.cameraheight, cam.camerawidth), np.float32)
frame_pre_1 = np.zeros((cam.cameraheight, cam.camerawidth), np.uint8)
frame_pre_3 = np.zeros((cam.cameraheight, cam.camerawidth, 3), np.uint8)
x_pre  = cam.camerawidth/2
y_pre  = cam.cameraheight/2
"""
1.尝试背景剪除法，直接剪除背景，不用二值化 效果见/Desktop/1.png
2.尝试黑白帧差法,考虑运动速度，建议用此法,效果见/Desktop/2.png
2+.测试黑白帧差法的速度,注意到网球的颜色较浅，与背景颜色近似，剪除效果不佳
3.编写黑白帧差法获得运动方向的算法
"""
count = 0
cam.get_image()
bkg = cv2.cvtColor(cam.frame, cv2.COLOR_BGR2GRAY)
while(True):
    cam.get_image()
    cam.frame = cv2.cvtColor(cam.frame, cv2.COLOR_BGR2GRAY)
    for i in range(1):
        cam.frame = cv2.GaussianBlur(cam.frame, (7 ,7), 0, 0)
#    cam.frame = cv2.cvtColor(cam.frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.absdiff(cam.frame , frame_pre_1)
    ret, cam.mask = cv2.threshold(frame, 100, 255, cv2.THRESH_BINARY)
    frame_pre_1 = cam.frame
    cv2.imwrite("/saved/"(str)(count)+".png",cam.mask)
    count = count + 1
    
    

    #cam.prehandle_image()
    #cam.findcenter_image()
    #detect the glob
    #if cam.moments['m00'] != 0:
    #    cv2.line(cam.frame, (cam.centerx,cam.centery), (x_pre, y_pre), (255,0,0),3) 
    #    cv2.imshow('catch',cam.mask)
    #    cam.show_image()
    #    cv2.waitKey(1)
    #    mask_pre = cam.mask 
    #    result = cam.generate_output(point2 = {'x':cam.centerx,'y':cam.centery}, point1 = {'x':x_pre,'y':y_pre}) 
    #    x_pre = cam.centerx
    #    y_pre = cam.centery
    #    print result['angle'],(cam.centerx,cam.centery),(x_pre,y_pre)
    #     
    #    car.send_cmd(50, result['angle'])
    #    car.wait_button(0, 's')
    #    car.send_cmd(0, 0)
    """
    TODO:
    using difference method
    """


