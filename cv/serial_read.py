import serial
import sys
import time

with serial.Serial('/dev/ttyUSB0',115200)  as ser:
    while(True):
        data = ser.readline()
        print data
	#print len(data)
	time.sleep(0.001)
        if len(data) >= 5:
            if (data[0] == '#'):
                data = data[1:]
                data = data[:-3]
                data = data.split('*')
                print data, (int)(data[0]), (int)(data[1])
                ser.flush
	    else:
		ser.close()
		time.sleep(0.001)
		ser.open()
	else:
	    ser.close()
	    time.sleep(0.001)
	    ser.open()
		
	
