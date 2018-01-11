# -*- coding: utf-8 -*-
# importation des librairies
"""http://www.tangentex.com/TraitementImages.htm
http://effbot.org/imagingbook/image.htm"""
import sys
from PIL import Image
"""from scipy import misc"""
from numpy import sqrt

def Norme(p1,p2,p3,p4):
    n = sqrt((p1[0]-p3[0])*(p1[0]-p3[0]) + (p2[0]-p4[0])*(p2[0]-p4[0]))    
    return n
    


# ouverture du fichier image

ImageFile = 'ovalé.png'

try:

  img = Image.open(ImageFile)

except IOError:

  print ('Erreur')

  sys.exit(1)

# affichage des caractéristiques de l'image

# récupération de la largeur et hauteur de l'image
colonne,ligne = img.size

# création des images intermédiaires

imgC = Image.new(img.mode,img.size)
imgD = Image.new(img.mode,img.size)

# transformation de l'image couleur en niveau de gris
for i in range(ligne):
    for j in range(colonne):
        pixel = img.getpixel((j,i)) # récupération du pixel
        # calcul du poids de chaque composante du gris dans le pixel (CIE709)
        if pixel[0]>150 and pixel[1]<150:
            p=(255,0,0)            
            imgC.putpixel((j,i),p)
imgC.show()

for i in range(ligne):
    left=0
    right=0
    j=0
    k=0
    while imgC.getpixel((j,i))[0]!=255 and j<colonne-1:
         j=j+1
    if imgC.getpixel((j,i))[0]==255:
        left=j
        
    while imgC.getpixel((colonne-k-1,i))[0]!=255 and k<colonne-1:
         k=k+1
    if imgC.getpixel((colonne-k-1,i))[0]==255:
        right=colonne-k
    if left!=0:
        p=(255,0,0)   
        for l in range(left,right):
            imgD.putpixel((l,i),p)

imgD.show()