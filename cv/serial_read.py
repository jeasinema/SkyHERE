import serial
import sys

with serial.Serial('/dev/ttyUSB0',115200)  as ser:
    while(True):
        data = ser.readall()
        print data
        if len(data) >= 5:
            if (data[0] == '#'):
                data = data[1:]
                data = data[:-3]
                data = data.split('*')
                print data, data[0], data[1]
                ser.flush
