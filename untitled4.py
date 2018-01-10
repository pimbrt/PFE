from PIL.Image import *
from skimage import io

def mystere(i):
    (l, h) = i.size
    for y in range(h):
        for x in range(l):
            c = Image.getpixel(i, (x, y))
            inv = 255 - c
            Image.putpixel(i, (x, y), inv)

i=open("tete.jpg")
#Image.show(i)

mystere(i)
Image.show(i)
io.imsave('tetes.jpg',i)#on enregistre la nouvelle photo 
