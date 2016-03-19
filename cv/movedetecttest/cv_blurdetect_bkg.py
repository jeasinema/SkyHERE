# -*- coding:UTF-8 -*-
import cv2
import numpy as np
from cv_interface import videoHandle as myv

threshold = 30
cam  = myv(0)
#cam.select_image_color()
#cv2.destroyAllWindows()
mask_pre = np.zeros((80, 60), np.uint8)
x_pre  = cam.camerawidth/2
y_pre  = cam.cameraheight/2
cam.get_image()
bkg = cam.frame
while(True):
    cam.get_image()
    #line18-19 can be swaped
    cam.frame = cv2.absdiff(cam.frame, bkg)
    cam.frame_resize = cv2.resize(cam.frame, (80, 60))
    #cam.mask = cv2.threshold(cam.frame_resize, threshold , 255, cv2.THRESH_BINARY)[1]
    ret, cam.mask = cv2.threshold(cam.frame, threshold , 255, cv2.THRESH_BINARY)
	print cam.mask, cam.mask.shape
    #cam.findcenter_image()
    #detect the glob
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
