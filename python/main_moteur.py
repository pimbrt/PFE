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
import RPi.GPIO as GPIO
import conn_db as cdb
moteur = motor.Moteur()


def moveMotors(angle_needed,angle_have):
    angle = angle_needed-angle_have
    if angle > 0:
        start = time.time()
        #tant que l'écart n'est pas corrigé
        while angle_have < angle_needed:
           moteur.moteur1(1)
           #moteur.reverse_Moteur1(1)
           #on situe la tête du bébé
           ov.find_ovale_2()
           mon_fichier = open("angle_moteur.txt", "r")
           angle_have=trait_image.arrondi(mon_fichier.read())
           mon_fichier.close
           if time.time()-start>=60:
               sql = """\
               UPDATE `datas` SET 'alert'=1  enfant_id = """+str(enfant_id)
               cdb.send_to_db(sql)
               break
           if GPIO.input(13)==1:
               break
            
        time_loop = time.time() - start
        moteur.stop_Moteur()
        # on retourne en arrière
        start=time.time()
        while time.time()-start<time_loop+2 :
            ov.find_ovale_2()
            moteur.reverse_Moteur1(1)
            #moteur.moteur1(1)
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
            if time.time()-start>=60:
               sql = """\
               UPDATE `datas` SET 'alert'=1  enfant_id = """+str(enfant_id)
               cdb.send_to_db(sql)
               break
            if GPIO.input(13)==1:
               break
        time_loop = time.time()-start
        moteur.stop_Moteur()
        start=time.time()
        while time.time()-start<time_loop+2:
            ov.find_ovale_2()
            moteur.reverse_Moteur2(1)
            #moteur.moteur2(1)
        moteur.stop_Moteur()
    else:
        moteur.stop_Moteur()

