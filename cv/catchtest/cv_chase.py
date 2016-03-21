# -*- coding:UTF-8 -*-
import cv2
import numpy as np
from cv_interface import videoHandle as myv
from move_interface import carHandle as myc

cam = myv(0)
car = myc(0)

cam.select_image_color()
cv2.destroyAllWindows()
mask_pre = np.zeros((640, 480), np.uint8)
x_pre = cam.camerawidth/2
y_pre = cam.cameraheight/2
while(True):
    cam.get_image()
    #cam.prehandle_image(size = (80, 60))
	
    cam.prehandle_image()
    cam.findcenter_image()
    #detect the glob
    if cam.moments['m00'] != 0:
        #cv2.line(cam.frame, (cam.centerx,cam.centery), (x_pre, y_pre), (255,0,0),3) 
        mask_pre = cam.mask 
        result = cam.generate_output(point2 = {'x':cam.centerx,'y':cam.centery}, point1 = {'x':x_pre,'y':y_pre}) 
        x_pre = cam.centerx
        y_pre = cam.centery
        print result['angle'],result['length'],(cam.centerx,cam.centery),(x_pre,y_pre)
    cv2.imshow('catch',cam.mask)
    cam.show_image()
    cv2.waitKey(1) 
    """
    测一下length的大小
    """
    #car.send_cmd(result['length'], result['angle'])
    """
    TODO:
    using difference method
    """
