# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 13:33:36 2018

@author: Maximilien
"""
import cv2
import numpy as np
def pre_traitement(image):
    kernel = np.ones((50,50),np.uint8)
    image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) # transformation en gris
    image_canny = cv2.Canny(image_gray,70,70)#Je sais pas trop à quoi ça sert mais sans ça ne marche pas
    image_final = cv2.morphologyEx(image_canny, cv2.MORPH_CLOSE, kernel)
    return image_final

def erode(grey_scale,kernel,number_it):
    return cv2.erode(grey_scale,kernel,iterations =number_it)

def dilate(grey_scale,kernel,number_it):
    return cv2.dilate(grey_scale,kernel,iterations = number_it)

def second_trait(grey_scale,kernel,processed):
    processed=erode(grey_scale,kernel,30)
    processed=dilate(grey_scale,kernel,3)
    processed=cv2.Canny(processed,100,100)
    return processed