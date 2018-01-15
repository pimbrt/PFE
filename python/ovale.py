#!/usr/bin/python3.6
# -*-coding:Latin-1 -*
import cv2
import numpy as np
from math import sin
from math import cos
from math import pi
#import database as db

class find_ovale:
    def __init__(self,orig):
        # create tmp images changer 3 ?
       #initialisation des valeus
        self.grey_scale = np.zeros((orig.shape[0],orig.shape[1],3),np.uint8)
        self.processed = np.zeros((orig.shape[0],orig.shape[1],3),np.uint8)
        self.kernel = np.ones((2,2),np.uint8)
        
        #passagede l'image en RGB et on blur orig
        orig=self.blur(orig,3)
        
        
        self.grey_scale=orig
    
        self.processed=self.erode(2)
        self.processed=self.dilate(2)
        self.processed=cv2.Canny(self.processed,100,200)
        
        cnt=self.find_contour()
        
        box=self.draw_contours(cnt)
        cv2.ellipse(orig,box,(0,0,200), 2)
        print(box)
        cv2.line(orig,(int(box[0][0]),int(box[0][1])),(int(box[0][0]+sin(0)*box[1][1]/2),int(box[0][1]-cos(0)*box[1][1]/2)),(0,255,0),2)
        cv2.line(orig,(int(box[0][0]),int(box[0][1])),(int(box[0][0]-sin(180*box[2]/pi)*box[1][1]/2),int(box[0][1]-cos(180*box[2]/pi)*box[1][1]/2)),(0,255,0),2)
        print('*******OVALE...OK')
        print("ANGLE: ")
        print(int(box[2]))
        
        #on envoie le résultat à la base de données
        #angle=box[2]+90
        #db.database(angle)


        '''
        To draw the ellipse, we need to pass several arguments. One argument is the center location (x,y). Next argument is axes lengths (major axis length, minor axis length). angle is the angle of rotation of ellipse in anti-clockwise direction. startAngle and endAngle denotes the starting and ending of ellipse arc measured in clockwise direction from major axis. i.e. giving values 0 and 360 gives the full ellipse. For more details, check the documentation of cv2.ellipse(). Below example draws a half ellipse at the center of the image.
'''
        # show images
        cv2.imwrite('tmp.jpg',orig)
        cv2.imshow("",orig)
        cv2.waitKey(0)
    
            
        
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
    

find_ovale(cv2.imread("image/fig2.jpg"))