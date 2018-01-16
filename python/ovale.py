#!/usr/bin/python3.6
# -*-coding:Latin-1 -*
import cv2
import numpy as np
from math import sin
from math import cos
from math import pi
from math import sqrt
import database as db

class find_ovale:
    def __init__(self,orig,first_pic_or_second):
        # create tmp images changer 3 ?
       #initialisation des valeus
        self.grey_scale = np.zeros((orig.shape[0],orig.shape[1],3),np.uint8)
        self.processed = np.zeros((orig.shape[0],orig.shape[1],3),np.uint8)
        self.final = np.zeros((orig.shape[0],orig.shape[1],3),np.uint8)
        self.kernel = np.ones((2,2),np.uint8)
        
        #passagede l'image en RGB et on blur orig
        orig=self.blur(orig,3)
        
        
        self.grey_scale=orig
    
        self.processed=self.erode(2)
        self.processed=self.dilate(2)
        self.processed=cv2.Canny(self.processed,100,200)
        
        cnt=self.find_contour()
        
        box=self.draw_contours(cnt)
        cv2.ellipse(self.final,box,(0,0,200), 2)
        cv2.line(self.final,(self.arrondi(box[0][0]),self.arrondi(box[0][1])),(self.arrondi(box[0][0]-sin(-pi+180*box[2]/pi)*box[1][1]/2),self.arrondi(box[0][1]-cos(-pi+180*box[2]/pi)*box[1][1]/2)),(255,0,0),2)
        cv2.line(self.final,(self.arrondi(box[0][0]),self.arrondi(box[0][1])),(self.arrondi(box[0][0]-sin(180*box[2]/pi)*box[1][1]/2),self.arrondi(box[0][1]-cos(180*box[2]/pi)*box[1][1]/2)),(255,0,0),2)
        cv2.line(self.final,(self.arrondi(box[0][0]),self.arrondi(box[0][1])),(self.arrondi(box[0][0]-sin(180*box[2]/pi-pi/2)*box[1][0]/2),self.arrondi(box[0][1]-cos(180*box[2]/pi-pi/2)*box[1][0]/2)),(255,0,0),2)
        cv2.line(self.final,(self.arrondi(box[0][0]),self.arrondi(box[0][1])),(self.arrondi(box[0][0]-sin(180*box[2]/pi+pi/2)*box[1][0]/2),self.arrondi(box[0][1]-cos(180*box[2]/pi+pi/2)*box[1][0]/2)),(255,0,0),2)
        
        
        cv2.line(self.final,(self.arrondi(box[0][0]),self.arrondi(box[0][1])),(self.arrondi(box[0][0]-sin(pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),self.arrondi(box[0][1]-cos(pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2)),(0,255,0),2)
        cv2.line(self.final,(self.arrondi(box[0][0]),self.arrondi(box[0][1])),(self.arrondi(box[0][0]-sin(3*pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),self.arrondi(box[0][1]-cos(3*pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2)),(0,255,0),2)
        cv2.line(self.final,(self.arrondi(box[0][0]),self.arrondi(box[0][1])),(self.arrondi(box[0][0]-sin(-pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),self.arrondi(box[0][1]-cos(-pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2)),(0,255,0),2)
        cv2.line(self.final,(self.arrondi(box[0][0]),self.arrondi(box[0][1])),(self.arrondi(box[0][0]-sin(-3*pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),self.arrondi(box[0][1]-cos(-3*pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2)),(0,255,0),2)
        
        print('*******OVALE...OK')
        print("*******ANGLE: "+str(int(box[2])+90))

        #Calcul des diagonales ODR ODL
        print(int(box[0][0]-sin(pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),int(box[0][1]-cos(pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),int(box[0][0]-sin(-3*pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),int(box[0][1]-cos(-3*pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2))
        ODL = self.Norme(int(box[0][0]-sin(pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),int(box[0][1]-cos(pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),int(box[0][0]-sin(-3*pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),int(box[0][1]-cos(-3*pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2))
        ODR = self.Norme(int(box[0][0]-sin(3*pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),int(box[0][1]-cos(3*pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),int(box[0][0]-sin(-pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),int(box[0][1]-cos(-pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2))
        print('*******DIAGONAL_FRONTO_OCCIPITAL...OK')
        #on envoie le résultat à la base de données
        angle=box[2]+90
        db.database(angle,box[1],ODL,ODR,first_pic_or_second)


        # show images
        cv2.imwrite('tmp.jpg',self.final)
        cv2.imshow("",self.final)
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
    def Norme(self,p1,p2,p3,p4):
        n = sqrt((p1-p3)*(p1-p3) + (p2-p4)*(p2-p4))    
        return n
    def arrondi(self,nb):
        nb=str(nb).split('.')
        if int(nb[1])>=5:
            return int(nb[0])+1
        else:
            return int(nb[0])


#find_ovale(cv2.imread("image/fig2.jpg"),1)