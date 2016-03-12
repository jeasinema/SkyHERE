import cv2
import cv
import numpy as np
import types

class videoHandle():
    distortdist = np.array([[ 411.8740606 ,    0.        ,  303.41061317],
                            [   0.        ,  409.43354707,  253.78413993],
                            [   0.        ,    0.        ,    1.        ]])
    distortmtx = np.array([[-0.70529664,  0.62594239, -0.00286203, -0.00662238, -0.29993423]])
    def __init__(self,deviceName):    
        try:
            self.cap = cv2.VideoCapture(deviceName)
            if cap.isOpened():
                self.camerawidth = self.cap.get(cv.CV_CAP_PROP_FRAME_WIDTH)
                self.cameraheight = self.cap.get(cv.CV_CAP_PROP_FRAME_HEIGHT)
                return True
            else:
                raise IOError
        except IOError:
            print "Camera is not correctly init."
            del self

    def get_image(self, flags):
        try:
            ret, frame = self.cap.read()
            if ret == 0:
                raise IOError
            return frame
        except IOError:
            return 0
    
    def select_color(self):
        #cv2.destroyAllWindows()
        self.flag_select = 1
        cv2.namedWindow('select_color')
        cv2.setMouseCallback('select_color', self.select_point_callback)
        
        while(self.flag_select):
            self.get_image(self)
            self.show_image(self, 'select_color')
        print self.selectx, self.selecty
        cv2.destroyWindow('select_color')
    
    def select_point_callback(self, event ,x, y, flag, param):
        if(event == cv2.EVENT_LBUTTONDOWN):
            cv2.circle(self.frame, (x, y), 10, (255, 0, 0), 0)
            self.selectx = x
            self.selecty = y
            self.flag_select = 0 
        self.select_color_hsv = (cv2.cvtColor(self.frame, cv2.COLORBGR2HSV))[0][self.selectx,selecty,:] 

    def show_image(self,windowName):
        cv2.imwrite((str)(windowName), self.frame)
        cv2.waitKey(1)

    def save_image(self,fileName):
        cv2.imwrite((str)(fileName), self.frame)

    def prehandle_image(self, *args, **kw):
        #Gussian Blur
        kernelSize = kw['kernelSize']
        if kernelSize % 2 == 1 and kernelSize > 0:
            cv2.GaussianBlur(self.image, (kernelSize, kernelSize), 1)
        else:
            print "no invalid kernelSize, use default one"
            cv2.GaussianBlur(self.frame, (5, 5) ,1)

        
        #undistort
        self.frame = cv2.undistort(self.frame, self.distortmtx, self.distortdist)
      
        #2HSV
        self.frame_hsv = cv2.cvtColor(self.frame, cv2.COLORBGR2HSV)
        
        #resize
        size = kw['size']
        if type(size) == types.TupleType:
            self.frame_resize_hsv = cv2.resize(self.frame_hsv,size)
        else:
            self.frame_resize_hsv = cv2.resize(self.frame_hsv,(self.camerawidth, self.cameraheight))
        #threshold
        self.thresholdlow = np.array((self.select_color_hsv[0]-20, 0, 50))
        self.thresholdhigh = np.array((self.select_color_hsv[0]+20, 0, 2355))
        self.mask = cv2.inRange(self.frame_resize_hsv, self.thresholdlow, self.thresholdhigh)
        
        #morphlogy
        self.mask = cv2.morphologyEx(self.mask, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))

    def findcenter_image(self,**kw):
        self.moments = cv2.moments(self.mask)
        
        if ret['m00'] != 0:
            self.centerx= (int)((float)(ret['m10'])/(float)(ret['m00']))
            self.centery= (int)((float)(ret['m01'])/(float)(ret['m00']))
        else:
            self.centerx = 320 
	    self.centery = 240
        self.centerx = self.centerx
        self.centery = self.centery
    
    def findcontours_image(self, **kw):
        self.contours = cv2.findContours(self.mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]
        self.numofcontours = len(self.contours)
         
     



