import serial
import sys

with serial.Serial('/dev/tty.usbserial-A4439N8',115200)  as ser:
    while(True):
        data = ser.readline()
        #print data
        if len(data) >= 5:
            if (data[0] == '#'):
                data = data[1:]
                data = data[:-3]
                data = data.split('*')
                print data, data[0], data[1]
                ser.flush
