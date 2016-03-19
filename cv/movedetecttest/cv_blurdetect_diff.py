# -*- coding:UTF-8 -*-
import cv2
import numpy as np
from cv_interface import videoHandle as myv

threshold = 20
cam = myv(0)
mask_pre = np.zeros((80, 60, 3), np.uint8)
x_pre  = cam.camerawidth/2
y_pre  = cam.cameraheight/2
cam.get_image()
frame_pre =  cv2.resize(cam.frame, (80,60))

while(True):
    cam.get_image()
    cam.frame = cv2.resize(cam.frame, (80, 60))
    cam.mask = cv2.absdiff(cam.frame, frame_pre)
    frame_pre = cam.frame
    cam.mask = cv2.threshold(cam.mask, threshold, 255, cv2.THRESH_BINARY)
    #detect the glob
    contours = cv2.findContours(cam.mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]

    if cam.moments['m00'] != 0:
        #cv2.line(cam.frame, (cam.centerx,cam.centery), (x_pre, y_pre), (255,0,0),3) 
        mask_pre = cam.mask 
        result = cam.generate_output(point2 = {'x':cam.centerx,'y':cam.centery}, point1 = {'x':x_pre,'y':y_pre}) 
        x_pre = cam.centerx
        y_pre = cam.centery
        print result['angle'],(cam.centerx,cam.centery),(x_pre,y_pre)
    #cv2.imshow('catch',cam.mask)
    #cam.show_image()
    #cv2.waitKey(1)
    """
    TODO:
    using difference method
    """
