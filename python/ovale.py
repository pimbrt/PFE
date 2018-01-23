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
import trait_image

class find_ovale:
    def __init__(self,orig,first_pic_or_second):
        ##
        #Initialisation des tableaux qui nous serviront pour le traitement d'image
        ##
        self.grey_scale = np.zeros((orig.shape[0],orig.shape[1],3),np.uint8)
        self.processed = np.zeros((orig.shape[0],orig.shape[1],3),np.uint8)
        self.final = np.zeros((orig.shape[0],orig.shape[1],3),np.uint8)
        self.kernel = np.ones((2,2),np.uint8)

        ##
        #L'image reçue est floutée et donnée à grey_scale
        ##
        orig=self.blur(orig,3)
        self.grey_scale=orig
        
        ##
        #trait_image est un fichier possédant second_trait qui permet d'eroder, et dilater  
        ##
        self.processed=trait_image.second_trait(self.grey_scale,self.kernel,self.processed)
        
        ##
        #find_contour va trouver les contours de l'image processed
        ##
        cnt=self.find_contour()
        
        ##
        #self.final est l'image à afficher avec un ovale on lui donne orig 
        #afin d'avoir une superposition de l'image reçue ainsi que de l'ellipse
        ##
        self.final=orig
        
        ##
        #draw_contours donne des informations sur l'ellipse trouvée dans l'image
        ##
        box=self.draw_contours(cnt)
        
        ##
        #on trace l'ellipse sur self.final
        ##
        cv2.ellipse(self.final,box,(0,0,255), 2)
        
        
        ##
        #Ontrace la grande longueur ainsi que la petite de l'ellipse 
        #ainsi que les diagonales
        ##
        cv2.line(self.final,(self.arrondi(box[0][0]),self.arrondi(box[0][1])),(self.arrondi(box[0][0]+sin(-pi+180*box[2]/pi)*box[1][0]/2),self.arrondi(box[0][1]-cos(-pi+180*box[2]/pi)*box[1][0]/2)),(255,0,0),2)
        cv2.line(self.final,(self.arrondi(box[0][0]),self.arrondi(box[0][1])),(self.arrondi(box[0][0]+sin(180*box[2]/pi)*box[1][0]/2),self.arrondi(box[0][1]-cos(180*box[2]/pi)*box[1][0]/2)),(255,0,0),2)
        cv2.line(self.final,(self.arrondi(box[0][0]),self.arrondi(box[0][1])),(self.arrondi(box[0][0]+sin(180*box[2]/pi-pi/2)*box[1][1]/2),self.arrondi(box[0][1]-cos(180*box[2]/pi-pi/2)*box[1][1]/2)),(255,0,0),2)
        cv2.line(self.final,(self.arrondi(box[0][0]),self.arrondi(box[0][1])),(self.arrondi(box[0][0]+sin(180*box[2]/pi+pi/2)*box[1][1]/2),self.arrondi(box[0][1]-cos(180*box[2]/pi+pi/2)*box[1][1]/2)),(255,0,0),2)
        cv2.line(self.final,(self.arrondi(box[0][0]),self.arrondi(box[0][1])),(self.arrondi(box[0][0]+sin(pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),self.arrondi(box[0][1]-cos(pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2)),(0,255,0),2)
        cv2.line(self.final,(self.arrondi(box[0][0]),self.arrondi(box[0][1])),(self.arrondi(box[0][0]+sin(3*pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),self.arrondi(box[0][1]-cos(3*pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2)),(0,255,0),2)
        cv2.line(self.final,(self.arrondi(box[0][0]),self.arrondi(box[0][1])),(self.arrondi(box[0][0]+sin(-pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),self.arrondi(box[0][1]-cos(-pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2)),(0,255,0),2)
        cv2.line(self.final,(self.arrondi(box[0][0]),self.arrondi(box[0][1])),(self.arrondi(box[0][0]+sin(-3*pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),self.arrondi(box[0][1]-cos(-3*pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2)),(0,255,0),2)
        print('*******OVALE...OK')
       
        ##
        #On enregistre l'angle de l'ellipse dans un fichier lorsqu'il s'agit 
        #de la première photo à analyser puis on soustrait le premier angle 
        #(celui enregistré dans le fichier) à l'angle trouvé ainsi on obtient 
        #le déplacement (à noter le premier angle donne l'angle de l'ellipse 
        #lorsque le bébé regarde au plafond ou plutot que ses parents 
        #maintiennent sa tête droite)
        ##
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

        ##
        #Calcul des diagonales ODR ODL
        ##
        ODL = self.Norme(int(box[0][0]-sin(pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),int(box[0][1]-cos(pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),int(box[0][0]-sin(-3*pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),int(box[0][1]-cos(-3*pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2))
        ODR = self.Norme(int(box[0][0]-sin(3*pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),int(box[0][1]-cos(3*pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),int(box[0][0]-sin(-pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),int(box[0][1]-cos(-pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2))
        print('*******DIAGONAL_FRONTO_OCCIPITAL...OK')
        
        
        ##
        #On envoit les résultats à la base de données
        ##
        db.database(angle,box[1],ODL,ODR,first_pic_or_second)

        #cv2.imshow("",self.final)
        #cv2.waitKey(0)
        
    def blur(self,orig,mask):
        return cv2.GaussianBlur(orig,(mask,mask),0)
    

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
   

