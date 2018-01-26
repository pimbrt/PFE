#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 13:33:36 2018

@author: Maximilien
"""
import cv2
import numpy as np
from math import sqrt
def pre_traitement(image):
    kernel = np.ones((40,40),np.uint8)
    image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    image_canny = cv2.Canny(image_gray,70,70)
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

def blur(orig,mask):
    return cv2.GaussianBlur(orig,(mask,mask),0)

def find_contour(processed):
    ret,thresh = cv2.threshold(processed,200,255,0)
    im2,contours,hierarchy = cv2.findContours(thresh, 1, 2)
    return contours

def draw_contours(contours):
    top_contours=0
    top_c=0
    for c in contours:
      # Number of points must be more than or equal to 6 for cv.FitEllipse2
      if len(c)>=6:
        if top_contours<=len(c):
            top_contours=len(c)
            top_c=c

    return cv2.fitEllipse(top_c)
                
def Norme(p1,p2,p3,p4):
    n = sqrt((p1-p3)*(p1-p3) + (p2-p4)*(p2-p4))    
    return n

def arrondi(nb):
    nb=str(nb).split('.')
    if int(nb[1])>=5:
        return int(nb[0])+1
    else:
        return int(nb[0])
