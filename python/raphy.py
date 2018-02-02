#!/usr/bin/python3.6
# -*- coding: latin 1 -*-
import cv2
import ovale
import pic
import trait_image
import RPi.GPIO as GPIO
import time


class take_pictures:
    def __init__(self):
        ##
        #Initialisation de first_pic_or_second dans le but de enregistrer 
        #l'angle "naturel" de la tête du bébé
        ##
        first_pic_or_second=1
        ##
        #Dans le fichier pic est contenue une fonction permettant de prendre 
        #une photo à l'aide de la raspberry
        ##
        self.img=pic.take_one_pic()
        print("IMAGE: IMPORTATION...OK")

        ##
        #give_me_ellipse est une fonction appartenant à cette classe, 
        #après traitement elle va envoyer l'image analysée à ovale.py qui 
        #va chercher l'ovale sur la photo
        ##
        self.img=self.give_me_ellipse(self.img,first_pic_or_second)
        print("*******ELLIPSE SAVED...OK")
        
        ##
        #first_pic_or_second pase à 2 indiquant aux autres fonctions qu'on 
        #cherche à trouver la variation d'angle entre la première et la 
        #dernière photo
        ##
        first_pic_or_second=2
        
        ##
        #La boucle permet de proposer de nouvelles photos à la fonction 
        #cherchant un ovale
        ##
        while 1==1:
            self.img=pic.take_one_pic()
            print("IMAGE_2: IMPORTATION...OK")
            self.img=self.give_me_ellipse(self.img,first_pic_or_second)
            print("*******ELLIPSE SAVED...OK")
            if GPIO.input(13)==1:
               break
            

    def give_me_ellipse(self,image,first_pic_or_second):
        image=trait_image.pre_traitement(image)
        print('*******PRE_TRAITEMENT...OK')
    
        image=cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        
        ovale.find_ovale(image,first_pic_or_second)
        image=cv2.imread('tmp.jpg')
        
        
        return image
   






"""
you can apply a horizontal and vertical flip
camera.hflip = True
camera.vflip = True


You can display a preview showing the camera feed on screen. 
Warning: this will overlay your Python session by default; 
if you have trouble stopping the preview, simply pressing Ctrl+D 
to terminate the Python session is usually enough to restore the display:
camera.start_preview()
camera.stop_preview()

Here the settings of the camera 
They can be changed

camera.sharpness = 0
camera.contrast = 0
camera.brightness = 50
camera.saturation = 0
camera.ISO = 0
camera.video_stabilization = False
camera.exposure_compensation = 0
camera.exposure_mode = 'auto'
camera.meter_mode = 'average'
camera.awb_mode = 'auto'
camera.image_effect = 'none'
camera.color_effects = None
camera.rotation = 0

camera.vflip = False
camera.crop = (0.0, 0.0, 1.0, 1.0)
"""

