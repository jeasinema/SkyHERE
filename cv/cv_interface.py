# -*- coding:UTF-8 -*- 
import cv2
import cv
import numpy as np
import types

class videoHandle:
    distortmtx = np.array([[ 411.8740606 ,    0.        ,  303.41061317],
                            [   0.        ,  409.43354707,  253.78413993],
                            [   0.        ,    0.        ,    1.        ]])
    distortdist = np.array([[-0.70529664,  0.62594239, -0.00286203, -0.00662238, -0.29993423]])
    def __init__(self, *args, **kw):    
        if len(args) > 0:
            deviceName = args[0]
        else:
            deviceName = 0
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
    
    def check_args(func):
        #if  len(func.argc) > 1:
        #    pass
        def wrappers(*args, **kwargs):
            
        func(*args, **kwargs)
        return wrappers
    def is_set(*args):
        try:
            for i in agrs:
                i
        except NameError:
            return 0
        else:
            return 1

    @check_2rgs
    def get_image(self, *args, **kw):
        try:
            ret, self.frame = self.cap.read()
            if ret == 0:
                raise IOError
            return self.frame
        except IOError:
            return 0
    
    @check_args
    def select_image_color(self):
        #cv2.destroyAllWindows()
        self.flag_select = 1
        cv2.namedWindow('select_color')
        cv2.setMouseCallback('select_color', self.select_point_callback)
        
        while(self.flag_select):
            self.get_image()
            self.show_image('select_color')
        if self.is_set(self.selectx, self.selecty, self.select_color_hsv):
            print self.selectx, self.selecty
            print self.select_color_hsv
        cv2.destroyWindow('select_color')
    
    @check_args
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


    @check_args
    def show_image(self, *args, **kw):
        if len(args) > 0:
            windowName = args[0]
        else:
            windowName = 'default'
        cv2.imshow((str)(windowName), self.frame)
        cv2.waitKey(1)

    @check_args
    def save_image(self, *args, **kw):
        if len(args) > 1:
            fileName = args[0]
        cv2.imwrite((str)(fileName), self.frame)

    @check_args
    def prehandle_image(self, *args, **kw):
        #Gussian Blur
        #if len(kw) > 0 and kw.has_key('kernelSize'):
        #    kernelSize = kw['kernelSize']
        #    if kernelSize % 2 == 1 and kernelSize > 0:
        #        self.frame = cv2.GaussianBlur(self.frame, (kernelSize, kernelSize), 1)
        #    else:
        #        self.frame = cv2.GaussianBlur(self.frame, (5, 5) ,1)
        #else:
        #    self.frame = cv2.GaussianBlur(self.frame, (5, 5) ,1)

        #undistort
        self.frame = cv2.undistort(self.frame, self.distortmtx, self.distortdist)

        #2HSV
        self.frame_hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        
        #resize
        if kw.has_key('size'):
            size = kw['size']
            if type(size) == types.TupleType:
                self.frame_resize_hsv = cv2.resize(self.frame_hsv,size)
            else:
                self.frame_resize_hsv = cv2.resize(self.frame_hsv,(self.camerawidth, self.cameraheight))
        else:
            self.frame_resize_hsv = cv2.resize(self.frame_hsv,(self.camerawidth, self.cameraheight))
        #threshold
        self.thresholdlow = np.array((self.select_color_hsv[0]-20, 120, 80))
        self.thresholdhigh = np.array((self.select_color_hsv[0]+20, 255, 255))
        self.mask = cv2.inRange(self.frame_resize_hsv, self.thresholdlow, self.thresholdhigh)
        
        #morphlogy
        self.mask = cv2.morphologyEx(self.mask, cv2.MORPH_OPEN, np.ones((7,7), np.uint8))
    
    @check_args
    def findcenter_image(self,**kw):
        self.moments = cv2.moments(self.mask)
        
        if self.moments['m00'] != 0:
            self.centerx= (int)((float)(self.moments['m10'])/(float)(self.moments['m00']))
            self.centery= (int)((float)(self.moments['m01'])/(float)(self.moments['m00']))
        else:
            self.centerx = 320 
	    self.centery = 240
        self.centerx = self.centerx
        self.centery = self.centery
    
    def findcontours_image(self, **kw):
        self.contours = cv2.findContours(self.mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]
        self.numofcontours = len(self.contours)
         
     



