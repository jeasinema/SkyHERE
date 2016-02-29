import numpy as np
import cv2
import glob
# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*7,3), np.float32)
#print objp
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
#print objp
# Arrays to store object points and image points from all the images. objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
objpoints = []
#images = glob.glob('*.png')+glob.glob('*.svg')+glob.glob('*.jpg')
images = glob.glob('*.png')
for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # Find the chess board corners
    cv2.imshow(fname,gray)
    cv2.waitKey(-1)
    cv2.destroyWindow(fname)
    ret, corners = cv2.findChessboardCorners(gray, (7,6),None)
    # If found, add object points, image points (after refining them)
    if ret == True: 
        print True
        objpoints.append(objp)
        #corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners)
        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, (7,6), corners,ret)
        cv2.imwrite('calib'+fname,img)
        cv2.imshow(fname+'Calib',img)
        cv2.waitKey(-1)
        cv2.destroyWindow(fname+'Calib')
       
cv2.destroyAllWindows()
