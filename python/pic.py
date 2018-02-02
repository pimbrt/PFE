#!/usr/bin/python3.6
# -*- coding: latin 1 -*-
import picamera
import cv2
import os


camera = picamera.PiCamera()
camera.capture('tmp.jpg')

def take_one_pic():
    camera.capture('tmp.jpg')
    image=cv2.imread('tmp.jpg')
    os.system("sudo mv tmp.jpg /var/www/html")
    return image



