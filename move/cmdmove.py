import cv2
import serial
import sys
import time

car = serial.Serial("/dev/ttyUSB0",9600)

while(True):
    key_input = raw_input()
    car.write("#"+(str)(key_input)+"*")
    time.sleep(0.1)
    print car.read()
    car.flush()


    
