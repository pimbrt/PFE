#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 14:08:11 2018

@author: pierre
"""
import motor.py as motor
import time

moteur = motor.Moteur()

def moveMotors(angle_needed,angle_have):

	angle = angle_needed-angle_have

	if angle > 0:
	    start = time.clock
	    while angle_have > angle_needed:
	        
	        moteur.moteur1(1)
	        
	        angle_have = find_ovale()
	    
	    time_loop = time.clock-start
	    moteur.stop_Moteur()
	    moteur.reverse_Moteur1(1)
	    time.sleep(time_loop)
	    moteur.stop_Moteur()
	    
	elif angle < 0:
	    start = time.clock
	    while angle_needed > angle_have:
	        
	        moteur.moteur2(1)
	        
	        angle_have = find_ovale()
	    
	    time_loop = time.clock-start
	    moteur.stop_Moteur()
	    moteur.reverse_Moteur2(1)
	    time.sleep(time_loop)
	    moteur.stop_Moteur()
	    
	else:
	    moteur.stop_Moteur()