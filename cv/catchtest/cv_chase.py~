# -*- coding:UTF-8 -*-
"""
using trad method to chase the object
"""
import cv2
import numpy as np
import time
import gc
from cv_interface import videoHandle as myv
from move_interface import carHandle as myc

max_speed = 60
result = {'angle':0}
cam = myv(0)
car = myc(0)
re_size = (120 ,90)
"""
disable the garbage collection
"""
gc.disable()


cam.select_image_color()
cv2.destroyAllWindows()
time.sleep(5)
print "start now"
while(True):
    cam.get_image()
    cam.prehandle_image(size = re_size)
	
    #cam.prehandle_image()
    cam.findcenter_image()
    #detect the glob
    if cam.moments['m00'] != 0:
        #cv2.line(cam.frame, (cam.centerx,cam.centery), (x_pre, y_pre), (255,0,0),3) 
        result = cam.generate_output(point2 = {'x':cam.centerx,'y':cam.centery}, point1 = {'x':re_size[0]/2,'y':re_size[1]/2}) 
    else:
		result = {'angle':result['angle'],'length':0}
    cv2.imshow('catch',cam.mask)
    #cam.show_image()
    cv2.waitKey(1) 
    print result['angle'],result['length'],(cam.centerx,cam.centery)
    """

    测一下length的大小:(320,0) -> length = 200
    				   (40,0) -> length = 30  speed*=3
					   (60,0) -> length = 45  speed*=2 
    距离小于多少时自动stop？
    ->(120,90) 大约20左右合适
    """
    speed = result['length']*2 + 30
    if speed < 60:
        speed = 0
    else:
        speed = (speed - 60) * 2
    if speed > max_speed:
        speed = max_speed
    car.send_cmd(speed , result['angle'])
	
