# -*- coding: utf-8 -*-
# importation des librairies
"""http://www.tangentex.com/TraitementImages.htm
http://effbot.org/imagingbook/image.htm"""
import cv2
import numpy as np

# ouverture du fichier image

class make_ellipse_full:
    def __init__(self,ImageFile):
        self.img1=ImageFile
        # récupération de la largeur et hauteur de l'image
        # récupération de la largeur et hauteur de l'image
        ligne = self.img1.shape[0]
        colonne = self.img1.shape[1]
        
        # création des images intermédiaires
        
        self.imgC = np.zeros((ligne,colonne,3),np.uint8)
        self.imgD = np.zeros((ligne,colonne,3),np.uint8)
        
        self.select_red(ligne,colonne)
        self.put_color(ligne,colonne)
        cv2.imwrite('tmp.jpg',self.imgD)
        
    def select_red(self,ligne,colonne):
        # transformation de l'image couleur en niveau de gris
        for i in range(ligne):
            for j in range(colonne):
                pixel = self.img1[i,j] # récupération du pixel
                # calcul du poids de chaque composante du gris dans le pixel (CIE709)
                if pixel[2]>150 and pixel[1]<150:
                    p=[0,0,255]         
                    self.imgC[i,j]=p
                    
    def put_color(self,ligne,colonne):
        for i in range(ligne):
            left=0
            right=0
            j=0
            k=0
            while self.imgC[i,j][2]!=255 and j<colonne-1:
                 j=j+1
            if self.imgC[i,j][2]==255:
                left=j
                
            while self.imgC[i,colonne-k-1][2]!=255 and k<colonne-1:
                 k=k+1
            if self.imgC[i,colonne-k-1][2]==255:
                right=colonne-k
            if left!=0:
                p=[0,0,255]  
                for l in range(left,right):
                    self.imgD[i,l]=p
                   
                    
                    
#ImageFile = cv2.imread('image/ovalons.jpg')
#make_ellipse_full(ImageFile)