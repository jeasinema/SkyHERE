import numpy as np
import cv2
import glob
# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*7,3), np.float32)
#print objp
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
objp = objp * 24.1
#print objp
# Arrays to store object points and image points from all the images. objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
objpoints = []
count = 0
#images = glob.glob('*.png')+glob.glob('*.svg')+glob.glob('*.jpg')
#images = glob.glob('*.png')
cap = cv2.VideoCapture(1)
while(True):
    try:
        ret, img = cap.read()
        if ret!=1:
            raise IOError
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        #ret,gray = cv2.threshold(gray,128,255,cv2.THRESH_BINARY)
    # Find the chess board corners
    #cv2.imshow(fname,gray)
    #cv2.waitKey(-1)
    #cv2.destroyWindow(fname)
        try:
            ret, corners = cv2.findChessboardCorners(gray, (7,6))
    # If found, add object points, image points (after refining them)
            if ret!=1:
                raise IOError
            #origin corner's dimension is 3
            corners = corners[:,0,:]
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
            #corners2 = corners
            imgpoints.append(corners2)
            # Draw and display the corners
            img = cv2.drawChessboardCorners(img, (7,6), corners2,ret)
            count = count + 1
            cv2.waitKey(-1)
        except IOError:
            pass
        cv2.namedWindow('vediocalib')
        cv2.imshow('Calib',img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if count == 10:
            cap.release()
            cv2.destroyAllWindows()
            #np.save("objpoints.npy", objpoints)
            #np.save("imgpoints.npy", imgpoints)
            print imgpoints
            break
    except IOError:
        continue
#try:
gray = cv2.imread('2.png')
gray = cv2.cvtColor(gray , cv2.COLOR_BGR2GRAY)
ret, mtx, dist, rvec, tvec = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
print mtx
print dist
cap = cv2.VideoCapture(1)
while(True):
    try:
        ret, img = cap.read()
        if ret!=1:
            raise IOError
        img = cv2.undistort(img , mtx , dist)
        cv2.namedWindow("undistorted")
        cv2.imshow('undistort',img)
        cv2.waitKey(1)
    except IOError:
        pass
    #    print "cap error"
    #    quit()
cv2.destroyAllWindows()   


