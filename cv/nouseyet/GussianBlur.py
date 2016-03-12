# -*- coding: UTF-8 -*-
# 用于产生高斯模糊
import cv2
import numpy as np

frame = cv2.imread('mvtest3.png')
level =  0
while(True):
    level = level + 1
    blur = cv2.GaussianBlur(frame, (level * 2 + 1, level * 2 + 1), sigmaX = 0, sigmaY = 0)
    cv2.imshow('blur', blur)
    cv2.imshow('frame', frame)
    print level
    cv2.waitKey(0)
