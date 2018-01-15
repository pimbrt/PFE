# -*- coding: utf-8 -*-
#Attention si probleme couleur utiliser cvtcolor from grey to RGB ? Bon juste les couleurs
#from PIL import Image, ImageDraw
import cv2
import numpy as np
from numpy import sqrt
class head_position:
    def __init__(self,ImageFile1,ImageFile2):
        # ouverture du fichier image
        
        self.img1 = ImageFile1
        self.img2 = ImageFile2

        
        # récupération de la largeur et hauteur de l'image
        ligne = self.img1.shape[0]
        colonne = self.img1.shape[1]
        
        # création des images intermédiaires
        self.imgS = np.zeros((ligne,colonne,3),np.uint8)
        self.head_size = self.find_head_size(ligne,colonne)
        
        cv2.imshow("image", self.imgS) 
        cv2.waitKey()
        
    def Norme(p1,p2,p3,p4):
        n = sqrt((p1[0]-p3[0])*(p1[0]-p3[0]) + (p2[0]-p4[0])*(p2[0]-p4[0]))    
        return n
    

    def find_head_size(self,ligne,colonne):
        
        seuilx1=0
        seuilx2=0
        seuily1=0
        seuily2=0
        i=0
        j=0
        while i<ligne:
            while j<colonne:
                pixel1 = self.img1[i,j] # récupération du pixel
                if pixel1[2]==255:
                    seuily1=i
                    seuilx1=j
                    i=ligne
                    j=colonne
                j=j+1
            i=i+1
        seuily2=ligne-1
        seuilx2=seuilx1
        return self.Norme(seuilx1,seuilx2,seuily1,seuily2)
    


    def determine_position(self,xmin,ymin,xmax,ymax):
 
        '''cv2.line(self.imgS,(xmin,ymin), (xmin,ymax),(0,0,255),2) 
        cv2.line(self.imgS,(xmin,ymin), (xmax,ymin),(0,0,255),2) 
        cv2.line(self.imgS,(xmax,ymax), (xmax,ymin),(0,0,255),2) 
        cv2.line(self.imgS,(xmax,ymax), (xmin,ymax),(0,0,255),2) 
        cv2.line(self.imgS,(xmin+int((xmax-xmin)/2),ymin), (xmin+int((xmax-xmin)/2),ymax),(0,0,255),2) 
        cv2.line(self.imgS,(xmax,ymin+int((ymax-ymin)/2)), (xmin,ymin+int((ymax-ymin)/2)),(0,0,255),2) 
        cv2.line(self.imgS,(xmin+int((xmax-xmin)/2),ymin+int((ymax-ymin)/2)), (xmin+3*int((xmax-xmin)/4),ymin),(0,0,255),2) 
        cv2.line(self.imgS,(xmin+int((xmax-xmin)/2),ymin+int((ymax-ymin)/2)), (xmin+1*int((xmax-xmin)/4),ymin),(0,0,255),2)
        '''
        



ImageFile1 = cv2.imread('image/fig1.jpg')
ImageFile2 = cv2.imread('image/fig2.jpg')
head_position(ImageFile1,ImageFile2)