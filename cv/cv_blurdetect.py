# -*- coding:UTF-8 -*-
import cv2
import numpy as np
from cv_interface import videoHandle as myv

cam  = myv(0)
cam.select_image_color()
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
        x_pre = cam.centerx
        y_pre = cam.centery


    






