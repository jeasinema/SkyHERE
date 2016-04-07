#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# ----------------------------------
# File Name : videorecord.py
# Purpose :
# Creation Date : 01-04-2016
# Last Modified : Fri Apr  1 21:00:50 2016
# Created By : Jeasine Ma
# ---------------------------------
import numpy as np
import cv2

cap = cv2.VideoCapture(0) 
# Define the codec and create VideoWriter object
fourcc = cv2.cv.FOURCC(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        frame = cv2.flip(frame,0)

    # write the flipped frame
    out.write(frame)

    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()

