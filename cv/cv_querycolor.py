#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# ----------------------------------
# File Name : cv_querycolor.py
# Purpose :
# Creation Date : 16-03-2016
# Last Modified : Wed Mar 16 20:01:19 2016
# Created By : Jeasine Ma
# ---------------------------------
from cv_interface import videoHandle as myv

if __name__ == "__main__":
	cam = myv(0)
        cam.select_image_color()
