# -*- coding: utf-8 -*-
#Attention si probleme couleur utiliser cvtcolor from grey to RGB ? Bon juste les couleurs
#from PIL import Image, ImageDraw
import cv2
import numpy as np

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
        ecart = self.find_ecart(ligne,colonne)
        xmin,ymin,xmax,ymax=self.substract_ellipse(ligne,colonne,ecart)
        cle,maxi = self.determine_position(xmin,ymin,xmax,ymax)
        print(cle,maxi)
        cv2.imshow("image", self.imgS) 
        cv2.waitKey()
        
        
    def find_ecart(self,ligne,colonne):
        '''
        N'importe quoi on  va changer
        '''
        seuilx1=0
        seuilx2=0
        seuily1=0
        seuily2=0
        for i in range(ligne):
            for j in range(colonne):
                pixel1 = self.img1[i,j] # récupération du pixel
                pixel2 = self.img2[i,j] # récupération du pixel
                if pixel1[2]==255 and seuily1<i:
                    seuily1=i
                    seuilx1=j
                if pixel2[2]==255 and seuily2<i:
                    seuily2=i
                    seuilx2=j
        ecart=0    
        if seuilx2-seuilx1>30:
            ecart=seuilx2-seuilx1
            
        return ecart
    
    def substract_ellipse(self,ligne,colonne,ecart):   
        xmax=0
        xmin=colonne
        ymax=0
        ymin=0
        done=0
        for i in range(ligne):
            for j in range(colonne-ecart):
                pixel1 = self.img1[i,j] # récupération du pixel
                pixel2 = self.img2[i,j+ecart] # récupération du pixel
             
                red=int(pixel2[2])-int(pixel1[2])
                green=int(pixel2[1])-int(pixel1[1])
                blue=int(pixel2[0])-int(pixel1[0])
            
                if red+green+blue>-50 and red+green+blue<50:#peut être grossit
                    p=[255,255,255]
                else:
                    if red>0: # on regarde si la forme vient de la première ou deuxième photo
                        p=[0,0,255]#RGB
                    else:
                        p=[0,255,0]#RGB
                    if done==0:
                        ymin=i
                        done=1
                    if xmin>j:
                        xmin=j
                    if xmax<j:
                        xmax=j
                    if ymax<i:
                        ymax=i
                
                self.imgS[i,j]= p
        #Enlever le noir provoquer par l'écarts
        for i in range(ligne):
            for j in range(colonne-ecart,colonne):
                p=[255,255,255]
                # composition de la nouvelle image
                self.imgS[i,j]= p
        return xmin,ymin,xmax,ymax


    def determine_position(self,xmin,ymin,xmax,ymax):
        tete={'top_left':0,'top_right':0,'bottom_left':0,'bottom_right':0,'centre':0}

        for i in range(ymin,ymin+int((ymax-ymin)/2)):
            for j in range(xmin,xmin+int((xmax-xmin)/2)):
                pixel = self.imgS[i,j] # récupération du pixel
            
                if pixel[1]==255 and pixel[0]==0:
                    tete['top_left']=tete['top_left']+1
            for j in range(xmin+int((xmax-xmin)/2),xmax):
                pixel = self.imgS[i,j] # récupération du pixel
        
                if pixel[1]==255 and pixel[0]==0:
                    tete['top_right']=tete['top_right']+1
                
        for i in range( ymin+int((ymax-ymin)/2),ymax):
            for j in range(xmin,xmin+int((xmax-xmin)/2)):
                pixel = self.imgS[i,j] # récupération du pixel
            
                if pixel[1]==255 and pixel[0]==0:
                    tete['bottom_left']=tete['bottom_left']+1
                    
            for j in range(xmin+int((xmax-xmin)/2),xmax):
                pixel = self.imgS[i,j] # récupération du pixel
            
                if pixel[1]==255 and pixel[0]==0:
                    tete['bottom_right']= tete['bottom_right']+1
        cv2.line(self.imgS,(xmin,ymin), (xmin,ymax),(0,0,255),2) 
        cv2.line(self.imgS,(xmin,ymin), (xmax,ymin),(0,0,255),2) 
        cv2.line(self.imgS,(xmax,ymax), (xmax,ymin),(0,0,255),2) 
        cv2.line(self.imgS,(xmax,ymax), (xmin,ymax),(0,0,255),2) 
        cv2.line(self.imgS,(xmin+int((xmax-xmin)/2),ymin), (xmin+int((xmax-xmin)/2),ymax),(0,0,255),2) 
        cv2.line(self.imgS,(xmax,ymin+int((ymax-ymin)/2)), (xmin,ymin+int((ymax-ymin)/2)),(0,0,255),2) 
        cv2.line(self.imgS,(xmin+int((xmax-xmin)/2),ymin+int((ymax-ymin)/2)), (xmin+3*int((xmax-xmin)/4),ymin),(0,0,255),2) 
        cv2.line(self.imgS,(xmin+int((xmax-xmin)/2),ymin+int((ymax-ymin)/2)), (xmin+1*int((xmax-xmin)/4),ymin),(0,0,255),2)
        
        maxi=0
        cle=""
        for key in tete:
            if tete[key]>maxi:
                maxi=tete[key]
                cle=key
        
        return cle,maxi


#ImageFile1 = cv2.imread('image/fig1.jpg')
#ImageFile2 = cv2.imread('image/fig2.jpg')
#head_position(ImageFile1,ImageFile2)