import cv2
import numpy as np


class find_ovale:
    def __init__(self,orig):
        # create tmp images
       
        self.grey_scale = np.zeros((orig.shape[0],orig.shape[1]),np.uint8)
        self.processed = np.zeros((orig.shape[0],orig.shape[1]),np.uint8)
        self.kernel = np.ones((2,2),np.uint8)
        
        orig=self.blur(orig,3)
        
        self.grey_scale=cv2.cvtColor(orig, cv2.COLOR_RGB2GRAY)
    
        self.processed=self.erode(2)
        self.processed=self.dilate(2)
        
        self.processed=cv2.Canny(self.processed,100,200)
        
        orig=self.blur(orig,1)
        
        cnt=self.find_contour()
        
        box=self.draw_contours(cnt)
        cv2.ellipse(orig,box,(0,0,200), 2)
        # show images
        cv2.imshow("image - press 'q' to quit", orig)
        #cv.ShowImage("post-process", processed)
        cv2.waitKey(-1)

        
    def blur(self,orig,mask):
        return cv2.GaussianBlur(orig,(mask,mask),0)
    
    def erode(self,number_it):
        return cv2.erode(self.grey_scale,self.kernel,iterations =number_it)

    def dilate(self,number_it):
        return cv2.dilate(self.grey_scale,self.kernel,iterations = number_it)

    def find_contour(self):

        ret,thresh = cv2.threshold(self.processed,127,255,0)
        im2,self.contours,hierarchy = cv2.findContours(thresh, 1, 2)
        return self.contours[0]
    
    def draw_contours(self,cnt):

        cv2.drawContours (self.processed, [cnt], 0,(0,0,255),3)
        
        top_contours=0
        for c in self.contours:
          # Number of points must be more than or equal to 6 for cv.FitEllipse2
          if top_contours<len(c):
              top_contours=len(c)
              top_c=c
        
        
        return cv2.fitEllipse(top_c)

# grab image
orig=cv2.imread('image/result1.jpg')
find_ovale(orig)