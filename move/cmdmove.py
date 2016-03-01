import cv2
import serial
import sys
import time

car = serial.Serial("/dev/ttyUSB1",9600)

while(True):
    key_input = raw_input()
    car.write("#"+(str)(key_input)+"*")
    car.flush()


    
