from PIL.Image import *
from skimage import io

def mystere(i):
    (l, h) = i.size
    for y in range(h):
        for x in range(l):
            c = Image.getpixel(i, (x, y))
            if c >= 150 :
                new = 255
            else :
                new = 0
    
            Image.putpixel(i, (x, y), new)

i=open("tete.jpg")
#Image.show(i)

mystere(i)
Image.show(i)
io.imsave('tetes.jpg',img)#on enregistre la nouvelle photo 
