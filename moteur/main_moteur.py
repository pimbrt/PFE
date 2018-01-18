#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 14:08:11 2018

@author: pierre
"""
import motor.py as motor

moteur = motor.Moteur()

#recupérer les angles
angle_needed=0
angle_have=0

angle = angle_needed-angle_have

if angle > 0:
    while angle_have > angle_needed:
        
        moteur.moteur1(1)
        
        angle_have = find_ovale()
        
    moteur.stop_Moteur()
    moteur.reverse_Moteur1(1)#trouver un moyen d'avoir le temps ou la longeur
    moteur.stop_Moteur()
    
elif angle < 0:
    while angle_needed > angle_have:
        
        moteur.moteur2(1)
        
        angle_have = find_ovale()
        
    moteur.stop_Moteur()
    moteur.reverse_Moteur2(1)#trouver un moyen d'avoir le temps ou la longeur
    moteur.stop_Moteur()
    
else:
    moteur.stop_Moteur()