# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 10:21:42 2018

@author: Maximilien
"""

import sys
from PIL import Image, ImageDraw
"""from scipy import misc"""
from numpy import sqrt

def Norme(p1,p2,p3,p4):
    n = sqrt((p1[0]-p3[0])*(p1[0]-p3[0]) + (p2[0]-p4[0])*(p2[0]-p4[0]))    
    return n
    

import matplotlib.pyplot as plt

# ouverture du fichier image

ImageFile1 = 'fig1.jpg'
ImageFile2 = 'fig2.jpg'

try:

  img1 = Image.open(ImageFile1)
  img2 = Image.open(ImageFile2)
except IOError:

  print ('Erreur')

  sys.exit(1)

# affichage des caractéristiques de l'image

# récupération de la largeur et hauteur de l'image
colonne,ligne = img1.size

# création des images intermédiaires
imgS = Image.new(img1.mode,img1.size)

xmax=0
xmin=colonne
ymax=0
ymin=0
done=0

seuilx1=0
seuilx2=0
seuily1=0
seuily2=0
for i in range(ligne):
    for j in range(colonne):
        pixel1 = img1.getpixel((j,i)) # récupération du pixel
        pixel2 = img2.getpixel((j,i)) # récupération du pixel
        if pixel1[0]==0 and seuily1<i:
            seuily1=i
            seuilx1=j
        if pixel2[0]==0 and seuily2<i:
            seuily2=i
            seuilx2=j
ecart=0    
if seuilx2-seuilx1>30:
    ecart=seuilx2-seuilx1
print (ecart)
# transformation de l'image couleur en niveau de gris
for i in range(ligne):
    for j in range(colonne-ecart):
        pixel1 = img1.getpixel((j,i)) # récupération du pixel
        pixel2 = img2.getpixel((j+ecart,i)) # récupération du pixel
        red=pixel2[0]-pixel1[0]
        green=pixel2[1]-pixel1[1]
        blue=pixel2[2]-pixel1[2]
    
        if red+green+blue>-50 and red+green+blue<50:#peut être grossit
            p=(255,255,255)
        else:
            if red>0: # on regarde si la forme vient de la première ou deuxième photo
                p=(255,0,0)
            else:
                p=(0,255,0)
            if done==0:
                ymin=i
                done=1
            if xmin>j:
                xmin=j
            if xmax<j:
                xmax=j
            if ymax<i:
                ymax=i
        imgS.putpixel((j,i), p)
for i in range(ligne):
    for j in range(colonne-ecart,colonne):
        p=(255,255,255)
        # composition de la nouvelle image
        imgS.putpixel((j,i), p)


plt.imshow(imgS)

tete={'top_left':0,'top_right':0,'bottom_left':0,'bottom_right':0}
draw = ImageDraw.Draw(imgS) 

draw.line((xmin,ymin, xmin,ymax), fill=128)
draw.line((xmin,ymin, xmax,ymin), fill=128)
draw.line((xmax,ymax, xmax,ymin), fill=128)
draw.line((xmax,ymax, xmin,ymax), fill=128)
draw.line((xmax,ymax, xmax,ymin), fill=128)
draw.line((xmin+int((xmax-xmin)/2),ymax, xmin+int((xmax-xmin)/2),ymin), fill=128)
draw.line((xmax,ymin+int((ymax-ymin)/2), xmin,ymin+int((ymax-ymin)/2)), fill=128)
for i in range(ymin,ymin+int((ymax-ymin)/2)):
    for j in range(xmin,xmin+int((xmax-xmin)/2)):
        pixel = imgS.getpixel((j,i)) # récupération du pixel
    
        if pixel[1]==255 and pixel[2]==0:
            tete['top_left']=tete['top_left']+1
    for j in range(xmin+int((xmax-xmin)/2),xmax):
        pixel = imgS.getpixel((j,i)) # récupération du pixel

        if pixel[1]==255 and pixel[2]==0:
            tete['top_right']=tete['top_right']+1
        
for i in range( ymin+int((ymax-ymin)/2),ymax):
    for j in range(xmin,xmin+int((xmax-xmin)/2)):
        pixel = imgS.getpixel((j,i)) # récupération du pixel
    
        if pixel[1]==255 and pixel[2]==0:
            tete['bottom_left']=tete['bottom_left']+1
            
    for j in range(xmin+int((xmax-xmin)/2),xmax):
        pixel = imgS.getpixel((j,i)) # récupération du pixel
    
        if pixel[1]==255 and pixel[2]==0:
            tete['bottom_right']= tete['bottom_right']+1
        
print (tete)
maxi=0
cle=""
for key in tete:
    if tete[key]>maxi:
        maxi=tete[key]
        cle=key

print(cle,maxi )
imgS.show()
