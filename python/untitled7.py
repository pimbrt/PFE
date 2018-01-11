
from skimage import io
from skimage import filters
import matplotlib.pyplot as plt
from skimage import exposure
from skimage import segmentation
from skimage import morphology



img = io.imread('teute.png', as_grey=True)#importation de la photo et mise en niveau de gris
io.imshow(img)
io.imsave('G_tete.pgm',img)#on enregistre la nouvelle photo 


simple_threshold = img > filters.threshold_otsu(img)

adaptive_threshold = filters.threshold_adaptive(img, 151)
filter_res = morphology.remove_small_objects(adaptive_threshold)
clear_image = segmentation.clear_border(filter_res)

plt.figure()
plt.subplot(221)
plt.imshow(img, cmap='gray')
plt.title('Image d\'origine')
plt.axis('off')
plt.subplot(222)
plt.imshow(simple_threshold, cmap='gray')
plt.title('Simple seuillage')
plt.axis('off')
plt.subplot(223)
plt.imshow(adaptive_threshold, cmap='gray')
plt.title('Seuillage adaptatif')
plt.axis('off')
plt.subplot(224)
plt.imshow(clear_image, cmap='gray')
plt.title('Image nettoyee')
plt.axis('off')

labels = morphology.label(clear_image, background=0)

plt.figure()
plt.imshow(labels, cmap='spectral')
plt.axis('off')

plt.show()