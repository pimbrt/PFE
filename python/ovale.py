#!/usr/bin/python3.6
# -*- coding: latin 1 -*-
import cv2
import numpy as np
from math import sin
from math import cos
from math import pi
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
        orig=trait_image.blur(orig,3)
        self.grey_scale=orig
        
        ##
        #trait_image est un fichier possédant second_trait qui permet d'eroder, et dilater  
        ##
        self.processed=trait_image.second_trait(self.grey_scale,self.kernel,self.processed)
        
        ##
        #find_contour va trouver les contours de l'image processed
        ##
        contours=trait_image.find_contour(self.processed)
        
        ##
        #self.final est l'image à afficher avec un ovale on lui donne orig 
        #afin d'avoir une superposition de l'image reçue ainsi que de l'ellipse
        ##
        self.final=orig

        ##
        #draw_contours donne des informations sur l'ellipse trouvée dans l'image
        ##
        box=trait_image.draw_contours(contours)
        
        ##
        #on trace l'ellipse sur self.final
        ##
        cv2.ellipse(self.final,box,(0,0,255), 2)
        
        
        ##
        #Ontrace la grande longueur ainsi que la petite de l'ellipse 
        #ainsi que les diagonales
        ##
        self.print_diag(box)
        print('*******OVALE...OK')
       
        ##
        #On enregistre l'angle de l'ellipse dans un fichier lorsqu'il s'agit 
        #de la première photo à analyser puis on soustrait le premier angle 
        #(celui enregistré dans le fichier) à l'angle trouvé ainsi on obtient 
        #le déplacement (à noter le premier angle donne l'angle de l'ellipse 
        #lorsque le bébé regarde au plafond ou plutot que ses parents 
        #maintiennent sa tête droite)
        ##
        angle=self.find_angle(first_pic_or_second,box)
        print("*******ANGLE: "+str(angle))

        ##
        #Calcul des diagonales ODR ODL
        ##
        ODL,ODR=self.calc_diag(box)
        print('*******DIAGONAL_FRONTO_OCCIPITAL...OK')
        
        
        ##
        #On envoit les résultats à la base de données
        ##
        db.database(angle,box[1],ODL,ODR,first_pic_or_second)

    def print_diag(self,box):
        cv2.line(self.final,(trait_image.arrondi(box[0][0]),trait_image.arrondi(box[0][1])),
                 (trait_image.arrondi(box[0][0]+sin(-pi+180*box[2]/pi)*box[1][0]/2),
                  trait_image.arrondi(box[0][1]-cos(-pi+180*box[2]/pi)*box[1][0]/2)),
                  (255,0,0),2)
        cv2.line(self.final,(trait_image.arrondi(box[0][0]),trait_image.arrondi(box[0][1])),
                 (trait_image.arrondi(box[0][0]+sin(180*box[2]/pi)*box[1][0]/2),
                  trait_image.arrondi(box[0][1]-cos(180*box[2]/pi)*box[1][0]/2)),
                  (255,0,0),2)
        cv2.line(self.final,(trait_image.arrondi(box[0][0]),trait_image.arrondi(box[0][1])),
                 (trait_image.arrondi(box[0][0]+sin(180*box[2]/pi-pi/2)*box[1][1]/2),
                  trait_image.arrondi(box[0][1]-cos(180*box[2]/pi-pi/2)*box[1][1]/2)),
                  (255,0,0),2)
        cv2.line(self.final,(trait_image.arrondi(box[0][0]),trait_image.arrondi(box[0][1])),
                 (trait_image.arrondi(box[0][0]+sin(180*box[2]/pi+pi/2)*box[1][1]/2),
                  trait_image.arrondi(box[0][1]-cos(180*box[2]/pi+pi/2)*box[1][1]/2)),
                  (255,0,0),2)
        cv2.line(self.final,(trait_image.arrondi(box[0][0]),trait_image.arrondi(box[0][1])),
                 (trait_image.arrondi(box[0][0]+sin(pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),
                  trait_image.arrondi(box[0][1]-cos(pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2)),
                  (0,255,0),2)
        cv2.line(self.final,(trait_image.arrondi(box[0][0]),trait_image.arrondi(box[0][1])),
                 (trait_image.arrondi(box[0][0]+sin(3*pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),
                  trait_image.arrondi(box[0][1]-cos(3*pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2)),
                  (0,255,0),2)
        cv2.line(self.final,(trait_image.arrondi(box[0][0]),trait_image.arrondi(box[0][1])),
                 (trait_image.arrondi(box[0][0]+sin(-pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),
                  trait_image.arrondi(box[0][1]-cos(-pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2)),
                  (0,255,0),2)
        cv2.line(self.final,(trait_image.arrondi(box[0][0]),trait_image.arrondi(box[0][1])),
                 (trait_image.arrondi(box[0][0]+sin(-3*pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),
                  trait_image.arrondi(box[0][1]-cos(-3*pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2)),
                  (0,255,0),2)
        
    def find_angle(self,first_pic_or_second,box):
        angle=box[2]
        if first_pic_or_second==1:
            first_angle=angle
            mon_fichier = open("fichier.txt", "w")
            mon_fichier.write(str(first_angle))
            mon_fichier.close()
        else:
            mon_fichier = open("fichier.txt", "r")
            first_angle=trait_image.arrondi(mon_fichier.read())
            mon_fichier.close
        angle=angle-first_angle
        if angle<-90:
            angle=angle+180
        if angle>90:
            angle=angle-180
        return angle
    
    def calc_diag(self,box):
        ODL = trait_image.Norme(int(box[0][0]-sin(pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),
                         int(box[0][1]-cos(pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),
                         int(box[0][0]-sin(-3*pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),
                         int(box[0][1]-cos(-3*pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2))
        ODR = trait_image.Norme(int(box[0][0]-sin(3*pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),
                         int(box[0][1]-cos(3*pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),
                         int(box[0][0]-sin(-pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2),
                         int(box[0][1]-cos(-pi/4+180*box[2]/pi)*(box[1][1]/2+box[1][0]/2)/2))
        return ODL,ODR
