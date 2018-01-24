#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import picamera
import cv2

camera = picamera.PiCamera()

def take_one_pic():
    
    camera.capture('tmp.jpg')
    return cv2.imread('tmp.jpg')
