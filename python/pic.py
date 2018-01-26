#!/usr/bin/python3.6
# -*- coding: latin 1 -*-
import picamera
import cv2

camera = picamera.PiCamera()
camera.capture('tmp.jpg')

def take_one_pic():
    camera.capture('tmp.jpg')
    return cv2.imread('tmp.jpg')



