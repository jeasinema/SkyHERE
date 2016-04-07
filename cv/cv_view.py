#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# ----------------------------------
# File Name : cv_view.py
# Purpose :
# Creation Date : 16-03-2016
# Last Modified : Tue Mar 29 18:27:20 2016
# Created By : Jeasine Ma
# ---------------------------------
from cv_interface import videoHandle as myv
import cv2

if __name__ == "__main__":
    cam = myv(0)
    while(True):
        cam.get_image()
        cam.frame = cv2.undistort(cam.frame, cam.distortmtx, cam.distortdist)
        cam.show_image()
        if cam.wait_button(1, 's'):
            cam.save_image()
            print "ok"
