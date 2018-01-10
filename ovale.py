import cv2
import numpy as np

# grab image
orig = cv2.imread('test6.png')

# create tmp images
grey_scale = np.zeros((orig.shape[0],orig.shape[1]),np.uint8)
processed = np.zeros((orig.shape[0],orig.shape[1]),np.uint8)

orig=cv2.GaussianBlur(orig,(3,3),0)

grey_scale=cv2.cvtColor(orig, cv2.COLOR_RGB2GRAY)

# do some processing on the grey scale image
kernel = np.ones((2,2),np.uint8)

processed=cv2.erode(grey_scale,kernel,iterations =10)
processed=cv2.dilate(grey_scale,kernel,iterations =5)

processed=cv2.Canny(processed,100,200)
#cv2.Canny(processed, processed, 5, 70, 3)
#cv2.Smooth(processed, processed, cv2.CV_GAUSSIAN, 15, 15)
processed=cv2.GaussianBlur(processed,(1,1),0)


#storage = cv.CreateMat(orig.width, 1, cv.CV_32FC3)

ret,thresh = cv2.threshold(processed,127,255,0)
im2,contours,hierarchy = cv2.findContours(thresh, 1, 2)
cnt = contours[0]

#contours = cv.FindContours(processed, storage, cv2.CV_RETR_EXTERNAL)

# N.B. 'processed' image is modified by this!

#contours = cv.ApproxPoly (contours, storage, cv.CV_POLY_APPROX_DP, 3, 1) 
# If you wanted to reduce the number of points...

cv2.drawContours (processed, [cnt], 0,(0,0,255),3)



for c in contours:
  # Number of points must be more than or equal to 6 for cv.FitEllipse2
  if len(c) >= 30:
    # Copy the contour into an array of (x,y)s
    box = cv2.fitEllipse(c)
    cv2.ellipse(orig,box,(0,0,200), 2)
# show images
cv2.imshow("image - press 'q' to quit", orig)
#cv.ShowImage("post-process", processed)
cv2.waitKey(-1)
