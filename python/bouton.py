#!/usr/bin/env python2.7
import RPi.GPIO as GPIO
import raphy
GPIO.setmode(GPIO.BCM)

# Le GPIO 23 est initialisé en entrée. Il est en pull-up pour éviter les faux signaux
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    GPIO.wait_for_edge(23, GPIO.FALLING)
    raphy.take_pictures()
    
except KeyboardInterrupt:
    GPIO.cleanup()       # reinitialisation GPIO lors d'une sortie CTRL+C
GPIO.cleanup()           # reinitialisation GPIO lors d'une sortie normale