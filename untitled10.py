
# -*- coding: Latin-1 -*-
# Programme d'extraction de contours dans une image
# Dominique Lefebvre pour TangenteX.com
# 8 janvier 2016
#

# importation des librairies
from numpy import sqrt
import sys
from PIL import Image,ImageFilter

def Norme(p1,p2,p3,p4):
    n = sqrt((p1[0]-p3[0])*(p1[0]-p3[0]) + (p2[0]-p4[0])*(p2[0]-p4[0]))    
    return n
    
# ouverture du fichier image
ImageFile = 'tete.jpg'
try:
   imgF = Image.open(ImageFile).convert('L')
except IOError:
    print ('Erreur sur ouverture du fichier ' + ImageFile)
    exit(1)

# récupération de la largeur et hauteur de l'image
colonne,ligne = img.size

# création des images intermédiaires
#imgF = Image.new(img.mode,img.size)
imgC = Image.new(img.mode,img.size)

## transformation de l'image couleur en niveau de gris
#for i in range(ligne):
#    for j in range(colonne):
##        pixel = img.getpixel((j,i)) # récupération du pixel
##        # calcul du poids de chaque composante du gris dans le pixel (CIE709)
##        gris = int(0.2125 * pixel[0] + 0.7154 * pixel[1] +  0.0721 * pixel[2])
##        # en gris les 3 composantes RGB sont identiques
##        p = (gris,gris,gris)
#        
#        # composition de la nouvelle image
#        imgF.putpixel((j,i), p)

# extraction des contours en niveau de gris
seuil = 30
for i in range(1,ligne-1):
    for j in range(1,colonne-1):
        p1 = img.getpixel((j-1,i))
        p2 = img.getpixel((j,i-1))
        p3 = img.getpixel((j+1,i))
        p4 = img.getpixel((j,i+1))
        n = Norme(p1,p2,p3,p4)
        if n < seuil:
            p = (255,255,255)
        else:
            p = (0,0,0)
        imgC.putpixel((j-1,i-1),p)

# la fonction de PIL qui fait la même chose
# imgF = img.filter(ImageFilter.CONTOUR)  

# affichage de l'image
imgC.show()

# fermeture du fichier image
img.close()
