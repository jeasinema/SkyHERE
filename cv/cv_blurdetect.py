import cv2
import numpy as np
from cv_interface import videoHandle as myv

cam  = myv(0)
cam.select_image_color()
mask_pre = np.zeros((cam.camerawidth, cam.cameraheight), np.float32)
while(True):
    cam.get_image()
    cam.prehandle_image()
    cam.show_image()
    #detect the glob
    if cam.moments['m00'] != 0:
        cv2.imshow('catch',com.mask - mask_pre)
        cv2.waitKey(0)
        mask_pre = cam.mask 

    






