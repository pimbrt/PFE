#!/usr/bin/python3.6
# -*-coding:Latin-1 -*
import cv2
import numpy as np
from math import sin
from math import cos
from math import pi
from math import sqrt
from math import acos

import cv2
import pic
import numpy as np


class find_ovale_2:
    def __init__(self):
        # create tmp images changer 3 ?
       #initialisation des valeus
        
        orig=pic.take_one_pic()

        orig=self.pre_traitement(orig)
        orig=cv2.cvtColor(orig, cv2.COLOR_GRAY2RGB)
        
        self.grey_scale = np.zeros((orig.shape[0],orig.shape[1],3),np.uint8)
        self.processed = np.zeros((orig.shape[0],orig.shape[1],3),np.uint8)
        self.final = np.zeros((orig.shape[0],orig.shape[1],3),np.uint8)
        self.kernel = np.ones((2,2),np.uint8)
        
        #passagede l'image en RGB et on blur orig
        orig=self.blur(orig,3)
        
        
        self.grey_scale=orig
        self.processed=self.pre_traitement(self.processed)
    
        self.processed=self.erode(30)
        self.processed=self.dilate(3)
        self.processed=cv2.Canny(self.processed,100,100)
        
        cnt=self.find_contour()

        ligne = self.final.shape[0]
        colonne = self.final.shape[1]

        self.final=orig
        box=self.draw_contours(cnt)
        
        angle=box[2]
        
        mon_fichier = open("fichier.txt", "r")
        first_angle=self.arrondi(mon_fichier.read())
        mon_fichier.close
        
        angle=angle-first_angle
        if angle <-90 or angle >90:
            print("ERROR: TOO FANTASTIC ANGLE")
        else:
       
            mon_fichier = open("previous_angle.txt", "r")
            previous_angle=self.arrondi(mon_fichier.read())
            mon_fichier.close
            if abs(angle-previous_angle)<50:
                mon_fichier = open("previous_angle.txt", "w")
                mon_fichier.write(str(angle))
                mon_fichier.close()

                mon_fichier = open("angle_moteur.txt", "w")
                mon_fichier.write(str(angle))
                mon_fichier.close()
               
                
                print("OVALE2 ANGLE: "+str(angle))
            else:
                print("ERROR TOO FAST")

    
            
        
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

    def pre_traitement(self,image):
        kernel = np.ones((50,50),np.uint8)
        image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) # transformation en gris
        image_canny = cv2.Canny(image_gray,70,70)#Je sais pas trop à quoi ça sert mais sans ça ne marche pas
        image_final = cv2.morphologyEx(image_canny, cv2.MORPH_CLOSE, kernel)
        return image_final

