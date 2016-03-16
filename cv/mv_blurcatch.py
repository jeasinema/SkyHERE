#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# ----------------------------------
# File Name : mv_blurcatch.py
# Purpose :
# Creation Date : 16-03-2016
# Last Modified : Wed Mar 16 12:06:42 2016
# Created By : Jeasine Ma
# ---------------------------------
import cv2
import serial
from functools import wraps
from cv_interface import videoHandle as myv
from move_interface import carHandle as myc
from decos_interface import decos

car = myc(0, 9600)
cam = myv(0)
cam.select_image_color()
car.send_cmd(0, 0)

mask_pre = np.zeros((cam.cameraheight, cam.camerawidth), np.float32)
x_pre  = cam.camerawidth/2
y_pre  = cam.cameraheight/2
while(True):
    cam.get_image()
    cam.prehandle_image()
    cam.findcenter_image()
    #detect the glob
    if cam.moments['m00'] != 0:
        cv2.line(cam.frame, (cam.centerx,cam.centery), (x_pre, y_pre), (255,0,0),3) 
        cv2.imshow('catch',cam.mask)
        cam.show_image()
        cv2.waitKey(1)
        mask_pre = cam.mask 
        result = cam.generate_output(point2 = {'x':cam.centerx,'y':cam.centery}, point1 = {'x':x_pre,'y':y_pre}) 
        x_pre = cam.centerx
        y_pre = cam.centery
        print result['angle'],(cam.centerx,cam.centery),(x_pre,y_pre)
         
        car.send_cmd(50, result['angle'])
        car.wait_button(0, 's')
        car.send_cmd(0, 0)
        """
        TODO:
        using difference method
        """
        
