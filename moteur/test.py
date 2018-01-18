#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 12:03:27 2018

@author: pierre
"""

import RPi.GPIO as io   
import time
io.setmode(io.BCM)  

# Constant values,   
PWM_MAX = 100 

io.setwarnings(False) 

# The pins configuration for Model B Revision 1.0   
leftMotor_DIR_pin = 22  
io.setup(leftMotor_DIR_pin, io.OUT)  
  
rightMotor_DIR_pin = 23  
io.setup(rightMotor_DIR_pin, io.OUT)  
  
io.output(leftMotor_DIR_pin, False)  

io.output(rightMotor_DIR_pin, False)  

leftMotor_PWM_pin = 17  
rightMotor_PWM_pin = 18  

io.setup(leftMotor_PWM_pin, io.OUT)  
io.setup(rightMotor_PWM_pin, io.OUT)  
  
# MAX Frequency 20 Hz  
leftMotorPWM = io.PWM(leftMotor_PWM_pin,20)  
rightMotorPWM = io.PWM(rightMotor_PWM_pin,20)  
  
leftMotorPWM.start(0)  
leftMotorPWM.ChangeDutyCycle(0)  

rightMotorPWM.start(0)  
rightMotorPWM.ChangeDutyCycle(0)  
  
leftMotorPower = 0  
rightMotorPower = 0  

io.output(rightMotor_DIR_pin, True)

rightMotorPower = PWM_MAX  
rightMotorPWM.start(1) 
rightMotorPWM.ChangeDutyCycle(PWM_MAX)

time.sleep(5)

io.output(rightMotor_DIR_pin, False)
rightMotorPower = 0
rightMotorPWM.start(0) 

io.output(leftMotor_DIR_pin, True)

leftMotorPower = PWM_MAX  
leftMotorPWM.start(1) 
leftMotorPWM.ChangeDutyCycle(PWM_MAX)

time.sleep(5)

io.output(leftMotor_DIR_pin, False)
leftMotorPower = 0
leftMotorPWM.start(0) 

