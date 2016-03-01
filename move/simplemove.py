import cv2
import serial
import sys

cap = cv2.VideoCapture(0)
car = serial.Serial("/dev/ttyUSB0",9600)

while(True):
    ret, frame  = cap.read()
    cv2.imshow('fpv', frame)
    cv2.waitKey(1)
    key_input = raw_input()
    if key_input == 'w':
        car.write("#30-0*")
        print key_input, "#30-0*"
    if key_input == 'a':
        car.write("30--90*")
        print key_input, "#30--90*"
    if key_input == 's':
        car.write("#30-180*")
        print key_input, "#30-180*"
    if key_input == 'd':
        car.write("#30-90*")
        print key_input, "#30-90*"
    if key_input == 'x':
	car.write("#0-0*")
	print key_input, "#0-0*"
    car.flush()

    
