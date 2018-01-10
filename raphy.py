import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('tete.png',0)
edges = cv2.Canny(img,100,200)

kernel = np.ones((5,5),np.uint8)

closing = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
clos2= cv2.morphologyEx(closing, cv2.MORPH_CLOSE, kernel)
autre = edges-closing
plt.subplot(151),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])

plt.subplot(152),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
#
#plt.subplot(143),plt.imshow(closing,cmap = 'gray')
#plt.title('closing  Image'), plt.xticks([]), plt.yticks([])
#
#plt.subplot(144),plt.imshow(clos2,cmap = 'gray')
#plt.title('closing2 Image'), plt.xticks([]), plt.yticks([])
#cv2.imwrite("result1.jpg", closing )
closing = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

plt.subplot(153),plt.imshow(closing,cmap = 'gray')
plt.title('openingImage'), plt.xticks([]), plt.yticks([])

sum=edges+closing
plt.subplot(154),plt.imshow(sum,cmap = 'gray')
plt.title('openingImage'), plt.xticks([]), plt.yticks([])

kernel = np.ones((2,2),np.uint8)
dilation = cv2.dilate(sum,kernel,iterations = 1)
plt.subplot(155),plt.imshow(dilation,cmap = 'gray')
plt.title('openingImage'), plt.xticks([]), plt.yticks([])
plt.show()



#import cv2
#import numpy as np
#
#img = cv2.imread('tete.jpg',0)
#kernel = np.ones((5,5),np.uint8)
#erosion = cv2.erode(img,kernel,iterations = 1)