import serial
import sys
import time

with serial.Serial('/dev/ttyUSB0',9600)  as ser:
    while(True):
        data = ser.read(30)
        print (str)(data)
        if len(data) >= 5:
            if (data[0] == '#'):
                data = data[1:]
                data = data[:-3]
                data = data.split('*')
                print data, data[0], data[1]
                ser.flush
                
