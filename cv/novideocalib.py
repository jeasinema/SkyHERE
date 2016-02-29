import numpy as np
import cv2
import glob
imgpoints = np.load("imgpoints.npy") # 2d points in image plane.
objpoints = np.load("objpoints.npy")
imgpoints = imgpoints[:,:,0:2]
#objpoints = objpoints[:,:,0:2]
img = []
obj = []
for i in imgpoints.reshape((420,2)):
    img.append(i)    
for i in objpoints:
    obj.append(i)
#print img
#print obj
#print imgpoints.shape
#print objpoints.shape
#print imgpoints
#print "++++++"
#print objpoints
#c=np.zeros((10,42,1),np.float32)
#imgpoints=np.c_[imgpoints,c]
#imgpoints = imgpoints.reshape((420,3)).tolist()
#objpoints = objpoints.reshape((420,3)).tolist()

#print imgpoints
#print "+++"
#print objpoints
#
gray = cv2.imread("2.png")
gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
#print imgpoints[1].size()
#print objpoints[1].size()
#print imgpoints.size()
#print objpoints.size()
#
print gray.shape[::-1]
ret, mtx, dist, rvec, tvec = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
print mtx
print dist
np.save('mtx.npy', mtx)
np.save('dist.npy', dist)
#images = glob.glob("*.png")
#for i in images:
#    img = cv2.imread(i)
#    img = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
#    ## undistort
#    dst = cv2.undistort(img, mtx, dist)
#    # crop the image
#    cv2.imwrite('calibresult.png',dst)
#    cv2.imshow('calib',dst)
#    cv2.waitKey(-1)   
#cv2.destroyAllWindows()
cap = cv2.VideoCapture(1)
a=0
flag=0
while(True):
    try:
        ret, img = cap.read()
        if ret!=1:
            raise IOError
        img = cv2.undistort(img , mtx , dist)
        cv2.namedWindow("undistorted")
        cv2.imshow('undistort',img)
        if cv2.waitKey(1) & 0xFF == ord('o'):
       #     flag=1 
       # if flag == 1:
            cv2.imwrite("./saved/"+(str)(a)+".png",img)
       #     a = a + 1
    except IOError:
        print "cap error"
        quit()
cv2.destroyAllWindows()   


