#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 13:33:28 2018

@author: pierre
"""

import RPi.GPIO as io 
io.setmode(io.BCM)  

# Constant values,   
PWM_MAX = 100 

io.setwarnings(False) 

motor2_DIR_pin = 22  
io.setup(motor2_DIR_pin, io.OUT)  
  
motor1_DIR_pin = 23  
io.setup(motor1_DIR_pin, io.OUT)  
  
io.output(motor2_DIR_pin, False)  

io.output(motor1_DIR_pin, False)  

motor2_PWM_pin = 17  
motor1_PWM_pin = 18  

io.setup(motor2_PWM_pin, io.OUT)  
io.setup(motor1_PWM_pin, io.OUT)  
  
# MAX Frequency 20 Hz  
motor2PWM = io.PWM(motor2_PWM_pin,20)  
motor1PWM = io.PWM(motor1_PWM_pin,20)  
  
motor2PWM.start(0)  
motor2PWM.ChangeDutyCycle(0)  

motor1PWM.start(0)  
motor1PWM.ChangeDutyCycle(0)

class Moteur:   
      
    def moteur1(self, pwr):
        power = pwr * PWM_MAX
        io.output(motor1_DIR_pin, True)
        motor1PWM.ChangeDutyCycle(power)
        
    def moteur2(self, pwr):
        power = pwr * PWM_MAX
        io.output(motor2_DIR_pin, True)
        motor2PWM.ChangeDutyCycle(power)
        
    def reverse_Moteur1(self, pwr):
        power = pwr * PWM_MAX
        io.output(motor1_DIR_pin, False)
        motor1PWM.ChangeDutyCycle(power)
        
    def reverse_Moteur2(self, pwr):
        power = pwr * PWM_MAX
        io.output(motor2_DIR_pin, False)
        motor2PWM.ChangeDutyCycle(power)
        
    def stop_Moteur(self):
        io.output(motor1_DIR_pin, False)
        motor1PWM.ChangeDutyCycle(0)
        
        io.output(motor2_DIR_pin, False)
        motor2PWM.ChangeDutyCycle(0)
