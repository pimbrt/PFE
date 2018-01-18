

"""
.. image:: PLOT2RST.current_figure

Ellipse detection
=================

In this second example, the aim is to detect the edge of a coffee cup.
Basically, this is a projection of a circle, i.e. an ellipse.
The problem to solve is much more difficult because five parameters have to be
determined, instead of three for circles.


Algorithm overview
------------------

The algorithm takes two different points belonging to the ellipse. It assumes
that it is the main axis. A loop on all the other points determines how much
an ellipse passes to them. A good match corresponds to high accumulator values.

A full description of the algorithm can be found in reference [1]_.

References
----------
.. [1] Xie, Yonghong, and Qiang Ji. "A new efficient ellipse detection
       method." Pattern Recognition, 2002. Proceedings. 16th International
       Conference on. Vol. 2. IEEE, 2002
"""




from skimage.transform import hough_ellipse
from skimage.draw import ellipse_perimeter

import cv2

# Load picture, convert to grayscale and detect edges
image_rgb = cv2.imread("image/fig1.jpg")
image_gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
edges = cv2.Canny(image_gray,80,80)

# Perform a Hough Transform
# The accuracy corresponds to the bin size of a major axis.
# The value is chosen in order to get a single high accumulator.
# The threshold eliminates low accumulators
result = hough_ellipse(edges, accuracy=20, threshold=250,
                       min_size=100, max_size=120)
result.sort(order='accumulator')

# Estimated parameters for the ellipse
print (result)
best = list(result[-1])
yc, xc, a, b = [int(round(x)) for x in best[1:5]]
orientation = best[5]

# Draw the ellipse on the original image
cy, cx = ellipse_perimeter(yc, xc, a, b, orientation)
image_rgb[cy, cx] = (0, 0, 255)
# Draw the edge (white) and the resulting ellipse (red)

edges=cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
edges[cy, cx] = (250, 0, 0)




cv2.imshow('orig',image_rgb)

cv2.imshow("Edge",edges)



"""
.. image:: PLOT2RST.current_figure

"""
