import cv2
import numpy as np

img = cv2.imread('tetes.jpg',0)
kernel = np.ones((5,5),np.uint8)
erosion = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)
plt.subplot(122),plt.imshow(erosion),plt.title('gardient')

tophat = cv2.morphologyEx(erosion, cv2.MORPH_TOPHAT, kernel)
plt.subplot(121),plt.imshow(tophat),plt.title('topat')

