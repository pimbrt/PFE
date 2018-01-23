#!/usr/bin/python3.6
# -*-coding:Latin-1 -*
import cv2
import numpy as np
from math import sin
from math import cos
from math import pi
from math import sqrt
from math import acos
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
    
        self.processed=self.erode(30)
        self.processed=self.dilate(3)
        self.processed=cv2.Canny(self.processed,100,100)
        
        cnt=self.find_contour()

        ligne = self.final.shape[0]
        colonne = self.final.shape[1]

        self.final=orig
        box=self.draw_contours(cnt)
        
        cv2.ellipse(self.final,box,(0,0,255), 2)
        
        cv2.line(self.final,(self.arrondi(box[0][0]),self.arrondi(box[0][1])),(self.arrondi(box[0][0]+sin(-pi+180*box[2]/pi)*box[1][0]/2),self.arrondi(box[0][1]-cos(-pi+180*box[2]/pi)*box[1][0]/2)),(255,0,0),2)
        cv2.line(self.final,(self.arrondi(box[0][0]),self.arrondi(box[0][1])),(self.arrondi(box[0][0]+sin(180*box[2]/pi)*box[1][0]/2),self.arrondi(box[0][1]-cos(180*box[2]/pi)*box[1][0]/2)),(255,0,0),2)
        cv2.line(self.final,(self.arrondi(box[0][0]),self.arrondi(box[0][1])),(self.arrondi(box[0][0]+sin(180*box[2]/pi-pi/2)*box[1][1]/2),self.arrondi(box[0][1]-cos(180*box[2]/pi-pi/2)*box[1][1]/2)),(255,0,0),2)
        cv2.line(self.final,(self.arrondi(box[0][0]),self.arrondi(box[0][1])),(self.arrondi(box[0][0]+sin(180*box[2]/pi+pi/2)*box[1][1]/2),self.arrondi(box[0][1]-cos(180*box[2]/pi+pi/2)*box[1][1]/2)),(255,0,0),2)
        
        
        cv2.line(self.final,(self.arrondi(box[0][0]),self.arrondi(box[0][1])),(self.arrondi(box[0][0]+sin(pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),self.arrondi(box[0][1]-cos(pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2)),(0,255,0),2)
        cv2.line(self.final,(self.arrondi(box[0][0]),self.arrondi(box[0][1])),(self.arrondi(box[0][0]+sin(3*pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),self.arrondi(box[0][1]-cos(3*pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2)),(0,255,0),2)
        cv2.line(self.final,(self.arrondi(box[0][0]),self.arrondi(box[0][1])),(self.arrondi(box[0][0]+sin(-pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),self.arrondi(box[0][1]-cos(-pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2)),(0,255,0),2)
        cv2.line(self.final,(self.arrondi(box[0][0]),self.arrondi(box[0][1])),(self.arrondi(box[0][0]+sin(-3*pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),self.arrondi(box[0][1]-cos(-3*pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2)),(0,255,0),2)
        
        print('*******OVALE...OK')
       
        #i,j,k,l,top=self.put_color(box,ligne,colonne)
        
        #angle=180*acos(self.Norme(k,l,i,l)/self.Norme(k,l,i,j))/pi
        angle=box[2]
        if first_pic_or_second==1:
            first_angle=angle
            mon_fichier = open("fichier.txt", "w")
            mon_fichier.write(str(first_angle))
            mon_fichier.close()
        else:
            mon_fichier = open("fichier.txt", "r")
            first_angle=self.arrondi(mon_fichier.read())
            mon_fichier.close
        print(angle)
        angle=angle-first_angle
       
        
        print("*******ANGLE: "+str(angle))

        #Calcul des diagonales ODR ODL
        print(int(box[0][0]-sin(pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),int(box[0][1]-cos(pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),int(box[0][0]-sin(-3*pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),int(box[0][1]-cos(-3*pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2))
        ODL = self.Norme(int(box[0][0]-sin(pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),int(box[0][1]-cos(pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),int(box[0][0]-sin(-3*pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),int(box[0][1]-cos(-3*pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2))
        ODR = self.Norme(int(box[0][0]-sin(3*pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),int(box[0][1]-cos(3*pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),int(box[0][0]-sin(-pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),int(box[0][1]-cos(-pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2))
        print('*******DIAGONAL_FRONTO_OCCIPITAL...OK')
        #on envoie le résultat à la base de données

        db.database(angle,box[1],ODL,ODR,first_pic_or_second)

        #cv2.imshow("",self.final)
        #cv2.waitKey(0)
        
    def blur(self,orig,mask):
        return cv2.GaussianBlur(orig,(mask,mask),0)
    
    def erode(self,number_it):
        return cv2.erode(self.grey_scale,self.kernel,iterations =number_it)

    def dilate(self,number_it):
        return cv2.dilate(self.grey_scale,self.kernel,iterations = number_it)

    def find_contour(self):

        ret,thresh = cv2.threshold(self.processed,200,255,0)
        im2,self.contours,hierarchy = cv2.findContours(thresh, 1, 2)

        return self.contours[0]
    
    def draw_contours(self,cnt):

        cv2.drawContours (self.processed, [cnt], 0,(0,0,255),3)
        
        top_contours=0
        top_c=0
        for c in self.contours:
          # Number of points must be more than or equal to 6 for cv.FitEllipse2
          if len(c)>=6:
            box=cv2.fitEllipse(c)
            #if 100*box[1][0]/box[1][1]>75 and box[1][0]>50 and box[1][0]<300 and box[1][1]<300:
            if top_contours<=len(c):
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
   

