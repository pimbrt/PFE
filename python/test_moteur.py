#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 14:08:11 2018

@author: pierre
"""
import motor as motor
import time
import ovale2 as ov
import trait_image
moteur = motor.Moteur()

def moveMotors(angle_needed,angle_have):
    angle = angle_needed-angle_have
    if angle > 0:
        start = time.time()
        while angle_have < angle_needed:
           moteur.moteur1(1)                
           ov.find_ovale_2()
           mon_fichier = open("angle_moteur.txt", "r")
           angle_have=trait_image.arrondi(mon_fichier.read())
           mon_fichier.close
            
        time_loop = time.time() - start
        moteur.stop_Moteur()
        moteur.reverse_Moteur1(1)
        time.sleep(time_loop)
        moteur.stop_Moteur()
    elif angle < 0:
        start = time.time()
        while angle_needed < angle_have:
            moteur.moteur2(1)
            #moteur.reverse_Moteur2(1)
            ov.find_ovale_2()
            mon_fichier = open("angle_moteur.txt", "r")
            angle_have=trait_image.arrondi(mon_fichier.read())
            mon_fichier.close
        time_loop = time.time()-start
        moteur.stop_Moteur()
        moteur.reverse_Moteur2(1)
        time.sleep(time_loop)
        moteur.stop_Moteur()
    else:
        moteur.stop_Moteur()

