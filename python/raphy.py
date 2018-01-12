import cv2
#import picamera
import numpy as np
import time
import ovale
import full_ellipse as fe
import Angle as agl



class take_pictures:
    def __init__(self):
        self.img=self.take_one_pic()
        print("FIRST IMAGE: IMPORTATION...OK")
        self.img=self.give_me_ellipse(self.img)
        print("FIRST IMAGE: ELLIPSE SAVED...OK")
        
        while 1==1:
            self.shoot()
            print("SECOND IMAGE: IMPORTATION...OK")
            self.img2=self.give_me_ellipse(self.img2)
            print("SECOND IMAGE: ELLIPSE SAVED...OK")
            cle,maxi,img3=agl.head_position(self.img,self.img2)
            print (cle,maxi)
            cv2.imshow("",img3)
            
            
    def pre_traitement(self,image):
        kernel = np.ones((15,15),np.uint8)
        image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) # transformation en gris
        image_canny = cv2.Canny(image_gray,150,150)#Je sais pas trop à quoi ça sert mais sans ça ne marche pas
        image_final = cv2.morphologyEx(image_canny, cv2.MORPH_CLOSE, kernel)
        return image_final
        
        
    def shoot(self):
        time.sleep(10)
        self.img2=self.take_one_pic()
        

    def take_one_pic(self):
        #camera = picamera.PiCamera()	
        #camera.capture('tmp.jpg')
        camera = cv2.VideoCapture(0)
        image = camera.read()[1]
        cv2.imwrite('tmp.jpg',image)
        return cv2.imread('tmp.jpg')

    def give_me_ellipse(self,image):
        image=self.pre_traitement(image)
        print('IMAGE: PRE_TRAITEMENT...OK')
        
        ovale.find_ovale(image)
        image=cv2.imread('tmp.jpg')
        print('IMAGE: OVALE...OK')
        
        image=fe.make_ellipse_full(image)
        image=cv2.imread('tmp.jpg')
        print('IMAGE: ELLIPSE...OK')
        return image
    


take_pictures()
"""
you can apply a horizontal and vertical flip
camera.hflip = True
camera.vflip = True


You can display a preview showing the camera feed on screen. 
Warning: this will overlay your Python session by default; 
if you have trouble stopping the preview, simply pressing Ctrl+D 
to terminate the Python session is usually enough to restore the display:
camera.start_preview()
camera.stop_preview()

Here the settings of the camera 
They can be changed

camera.sharpness = 0
camera.contrast = 0
camera.brightness = 50
camera.saturation = 0
camera.ISO = 0
camera.video_stabilization = False
camera.exposure_compensation = 0
camera.exposure_mode = 'auto'
camera.meter_mode = 'average'
camera.awb_mode = 'auto'
camera.image_effect = 'none'
camera.color_effects = None
camera.rotation = 0
camera.hflip = False
camera.vflip = False
camera.crop = (0.0, 0.0, 1.0, 1.0)
"""

