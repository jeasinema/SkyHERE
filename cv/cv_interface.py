# -*- coding:UTF-8 -*-
import cv2
import cv
import numpy as np
import types
import cmath
import time
from datetime import datetime
from functools import wraps
from decos_interface import decos

class videoHandle:
    distortmtx = np.array([[ 411.8740606 ,    0.        ,  303.41061317],
                            [   0.        ,  409.43354707,  253.78413993],
                            [   0.        ,    0.        ,    1.        ]])
    distortdist = np.array([[-0.70529664,  0.62594239, -0.00286203, -0.00662238, -0.29993423]])
    
    default_camera = 0
    
    @decos(1)
    def __init__(self, *args, **kwargs):    
        """
        args = (deviceName)
        default = (0)
        """
        if kwargs['tupvalid']:
            deviceName = args[0]
        else:
            deviceName = self.default_camera
        try:
            self.cap = cv2.VideoCapture(deviceName)
            if self.cap.isOpened():
                self.camerawidth = (int)(self.cap.get(cv.CV_CAP_PROP_FRAME_WIDTH))
                self.cameraheight = (int)(self.cap.get(cv.CV_CAP_PROP_FRAME_HEIGHT))
            else:
                raise IOError
        except IOError:
            print "Camera is not correctly init."
            del self
    @decos(0)
    def is_set(*args, **kwargs):
        """
        args = ()
        default = ()
        """
        try:
            for i in agrs:
                i
        except NameError:
            return 0
        else:
            return 1

    @decos(0)
    def get_image(self, *args, **kwargs):
        """
        args = ()
        default = ()
        """
        try:
            ret, self.frame = self.cap.read()
            if ret == 0:
                raise IOError
            return self.frame
        except IOError:
            return 0
    
    @decos(0)
    def select_image_color(self,*args, **kwargs):
        """
        args = ()
        default = ()
        """
        #cv2.destroyAllWindows()
        self.flag_select = 1
        cv2.namedWindow('select_color')
        cv2.setMouseCallback('select_color', self.select_point_callback)
        
        while(self.flag_select):
            self.get_image()
            self.frame = cv2.undistort(self.frame, self.distortmtx, self.distortdist)
            self.show_image('select_color')
        if self.is_set(self.selectx, self.selecty, self.select_color_hsv):
            print self.selectx, self.selecty
            print self.select_color_hsv
        cv2.destroyWindow('select_color')
    
    def select_point_callback(self, event , x, y, flag, param):
        self.select_color = self.frame[y,x,:] 
        self.select_color_hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)[y,x,:]
        if(event == cv2.EVENT_LBUTTONDOWN):
            cv2.circle(self.frame, (x, y), 10, (255, 0, 0), 1)
            self.selectx = x
            self.selecty = y
            self.flag_select = 0 
            self.select_color_hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)[y,x,:]
            cv2.waitKey(50)

#        print cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)[x,y,:]
        #if self.is_set(self.select_color):
        print x, y, self.select_color , self.select_color_hsv

    @decos(1)
    def show_image(self, *args, **kwargs):
        """
        args = (windowName)
        default = ('default')
        """
        if kwargs['tupvalid']:
            windowName = args[0]
        else:
            windowName = 'default'
        cv2.imshow((str)(windowName), self.frame)
        cv2.waitKey(1)

    @decos(1)
    def save_image(self, *args, **kwargs):
        """
        args = (fileName)
        default = (datetime.now().ctime())
        """
        if kwargs['tupvalid']:
            fileName = args[0]
        else:
            fileName = datetime.now().ctime()
        cv2.imwrite((str)(fileName)+'.png', self.frame)
        print fileName+" saved."

    @decos(1)
    def prehandle_image(self, *args, **kwargs):
        """
        kwargs = {'size':(size_x, size_y)}
        default = {'size': (vedioHandle.camerawidth,vedioHandle.cameraheight)}
        """
        try:
            if kwargs['dicvalid']:
                if kwargs.has_key('size'):
                    size = kwargs['size']
                    if type(size) == types.TupleType:
                        pass
                    else:
                        raise IOError 
                else:
                    raise IOError
            else:
                raise IOError
        except IOError:
            size  = (self.camerawidth, self.cameraheight)

        #undistort
        self.frame = cv2.undistort(self.frame, self.distortmtx, self.distortdist)
        
        #resize
        self.frame_resize = cv2.resize(self.frame,size)
      
        #2HSV
        self.frame_resize_hsv = cv2.cvtColor(self.frame_resize, cv2.COLOR_BGR2HSV)
        
        #threshold
        self.thresholdlow = np.array((self.select_color_hsv[0]-20, 120, 80))
        self.thresholdhigh = np.array((self.select_color_hsv[0]+20, 255, 255))
        self.mask = cv2.inRange(self.frame_resize_hsv, self.thresholdlow, self.thresholdhigh)
        
        #morphlogy
        self.mask = cv2.morphologyEx(self.mask, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))
    
    @decos(0)
    def findcenter_image(self,*args, **kwargs):
        """
        args = ()
        default = ()
        find the center of cam.mask
        """
        self.moments = cv2.moments(self.mask)
        
        if self.moments['m00'] != 0:
            self.centerx= (int)((float)(self.moments['m10'])/(float)(self.moments['m00']))
            self.centery= (int)((float)(self.moments['m01'])/(float)(self.moments['m00']))
        else:
            self.centerx = self.camerawidth/2
	    self.centery = self.cameraheight/2
        self.centerx = self.centerx
        self.centery = self.centery
    
    def findcontours_image(self, *args, **kwargs):
        self.contours = cv2.findContours(self.mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]
        self.numofcontours = len(self.contours)
         
    @decos(0,2)
    def generate_output(self,*args,**kwargs):
        """
        kwargs = {'point1' : {'x' : x, 'y' : y},'point2': {'x' : x, 'y' : y}}
        default = {'point1' : {'x' : camerawidth/2, 'y' : cameraheight/2},'point2': {'x' : camerawidth/2, 'y' : cameraheight/2}}
        ret = {'length' : length, 'angle' : angle}
        """
        length = 0
        angle = 0
        if kwargs['dicvalid']:
            try:
                p1 = kwargs['point1']
                p2 = kwargs['point2']
            except KeyError:
                p1 = {'x':self.camerawidth/2,'y':self.cameraheight/2} 
                p2 = p1
            length = np.linalg.norm([p2['x']-p1['x'],p2['y']-p1['y']])
            if p1['x'] == p2['x']:
                if p2['y'] > p1['y']:
                    angle = 180
                else:
                    angle = 0
            elif p1['y'] == p2['y']:
                if p2['x'] > p1['x']:
                    angle = 90
                else:
                    angle - 90
            else:        
                angle = np.arctan(((float)((p2['x'])-p1['x']))/((float)(p1['y']-p2['y'])))  #xaxis is reverse
                angle = (float)(angle) / cmath.pi * 180
                if (p2['y'] > p1['y']):
                    if (p2['x'] > p1['x']):
                        angle = 180 + angle
                    else:
                        angle = -180 + angle
        return {'length':length, 'angle':angle}

    @decos(2)
    def wait_button(self, *args, **kwargs):
        """
        args = (wait_time, wait_what)
        default = (0,'o')
        ret = 1(button == wait_what) 0(button != wait_what)

        """
        if kwargs['tupvalid']:
            if cv2.waitKey(args[0]) &  0xFF == ord((str)(args[1])):
                return 1
            else:
                return 0
        else:
            if cv2.waitKey(0) & 0xFF == ord((str)('o')):
                return 1
            else:
                return 0
