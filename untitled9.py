import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage
from PIL import Image 
import cv2


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

def plot(data, title):
    plot.i += 1
    plt.subplot(2,2,plot.i)
    plt.imshow(data)
    plt.gray()
    plt.title(title)
plot.i = 0

# Load the data...
im = Image.open('tete.jpg')
data = np.array(im, dtype=float)
plot(data, 'Original')
#
## A very simple and very narrow highpass filter
#kernel = np.array([[-1, -1, -1],
#                   [-1,  8, -1],
#                   [-1, -1, -1]])
#highpass_3x3 = ndimage.convolve(data, kernel)
#
#
## A slightly "wider", but sill very simple highpass filter 
#kernel = np.array([[-1, -1, -1, -1, -1],
#                   [-1,  1,  2,  1, -1],
#                   [-1,  2,  5,  2, -1],
#                   [-1,  1,  2,  1, -1],
#                   [-1, -1, -1, -1, -1]])
#highpass_5x5 = ndimage.convolve(data, kernel)
#

# Another way of making a highpass filter is to simply subtract a lowpass
# filtered image from the original. Here, we'll use a simple gaussian filter
# to "blur" (i.e. a lowpass filter) the original.
lowpass = ndimage.gaussian_filter(data, 2)
gauss_highpass = data - lowpass
plot(gauss_highpass, r'Gaussian Highpass, $\sigma = 3 pixels$')

plt.show()