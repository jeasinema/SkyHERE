import cv2
import serial
import numpy as np
from functools import wraps
from decos_interface import decos

class carHandle:

    default_angle = 0
    default_speed = 0
    defaule_serial = 0
    default_baudrate = 9600

    @decos(2)
    def __init__(self, *args, **kwargs):
        """
        args = (deviceName, baudrate)
        """
        if kwargs['tupvalid']:
            deviceName = (int)(args[0])
            baudrate = (int)(args[1])
        else:
            deviceName = self.defaule_serial
            baudrate = self.default_baudrate
        try:
            self.serial_device = serial.Serial("/dev/ttyUSB"+(str)(deviceName), baudrate)
        except serial.serialutil.SerialException:
            print "cannot open the serial port correctly."
            del self
    
    @decos(2)
    def send_cmd(self, *args, **kwargs):
        """
        args = (speed, angle)
        """
        if kwargs['tuplevalid']:
            speed = (int)(args[0])
            angle = (int)(args[1])
        else:
            speed = self.default_speed
            angle = self.default_angle
        try:
            self.serial_device.write("#"+(str)(speed)+"-"+(str)(angle))
        except srial.serialutil.SerialException:
            print "transfer failed."
    
    @decos(2)
    def wait_button(self, *args, **kwargs):
        """
        args = (wait_time, wait_what)
        default args is (0,'o')
        """
        if kwargs['tupvalid']:
            while(cv2.waitKey(args[0]) &  0xFF == ord((str)(args[1]))):
                pass
        else:
            while(cv2.waitKey(0) & 0xFF == ord((str)('o'))):
                pass

