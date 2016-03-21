#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# ----------------------------------
# File Name : cv_view.py
# Purpose :
# Creation Date : 16-03-2016
# Last Modified : Wed Mar 16 20:03:47 2016
# Created By : Jeasine Ma
# ---------------------------------
from cv_interface import videoHandle as myv

if __name__ == "__main__":
    cam = myv(0)
    while(True):
        cam.get_image()
        cam.show_image()
        if cam.wait_button(1, 's'):
            cam.save_image()
            print "ok"
