#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import pic
import trait_image


class find_ovale_2:
    #Voir commentaires de ovale
    def __init__(self):
        orig=pic.take_one_pic()

        orig=trait_image.pre_traitement(orig)
        orig=cv2.cvtColor(orig, cv2.COLOR_GRAY2RGB)
        
        self.grey_scale = np.zeros((orig.shape[0],orig.shape[1],3),np.uint8)
        self.processed = np.zeros((orig.shape[0],orig.shape[1],3),np.uint8)
        self.final = np.zeros((orig.shape[0],orig.shape[1],3),np.uint8)
        self.kernel = np.ones((2,2),np.uint8)
 
        orig=trait_image.blur(orig,3)
        
        self.grey_scale=orig
    
        self.processed=trait_image.second_trait(self.grey_scale,self.kernel,self.processed)
        
        contours=trait_image.find_contour(self.processed)

        self.final=orig
        box=trait_image.draw_contours(contours)
        
        angle=box[2]
        
        mon_fichier = open("fichier.txt", "r")
        first_angle=trait_image.arrondi(mon_fichier.read())
        mon_fichier.close
        
        angle=angle-first_angle
        if angle <-90 or angle >90:
            print("ERROR: TOO FANTASTIC ANGLE")
        else:
       
            mon_fichier = open("previous_angle.txt", "r")
            previous_angle=trait_image.arrondi(mon_fichier.read())
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

    
            
        



