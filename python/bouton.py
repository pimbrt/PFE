#!/usr/bin/env python2.7
# -*- coding: latin 1 -*-
#@lxterminal -e bash /home/pi/pfe/start.sh

import RPi.GPIO as GPIO
import raphy
import motor
import os
init=0
while 1==1:
    
    GPIO.setmode(GPIO.BCM)

    # Le GPIO 13 est initialisé en entrée. Il est en pull-up pour éviter les faux signaux
    GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    try:
        
        GPIO.wait_for_edge(13, GPIO.FALLING)
        raphy.take_pictures()
        init=0
        

    except KeyboardInterrupt:
        print ("ERROR 1")    # reinitialisation GPIO lors d'une sortie CTRL+C
