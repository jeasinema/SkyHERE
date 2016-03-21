#!/usr/bin/env python
import cv2
import serial
import sys
import time

car = serial.Serial("/dev/ttyUSB0",9600)
car.write("#0-0*")
car.flush()


    
