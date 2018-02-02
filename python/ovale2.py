#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import pic
import MySQLdb
import trait_image
from datetime import datetime
import conn_db as cdb

class find_ovale_2:
    #Voir commentaires de ovale
    def __init__(self):
        orig=pic.take_one_pic()

        orig=trait_image.pre_traitement(orig)
        orig=cv2.cvtColor(orig, cv2.COLOR_GRAY2RGB)
        
        self.grey_scale = np.zeros((orig.shape[0],orig.shape[1],3),np.uint8)
        self.processed = np.zeros((orig.shape[0],orig.shape[1],3),np.uint8)
        self.final = np.zeros((orig.shape[0],orig.shape[1],3),np.uint8)
        self.kernel = np.ones((2,2),np.uint8)
 
        orig=trait_image.blur(orig,3)
        
        self.grey_scale=orig
    
        self.processed=trait_image.second_trait(self.grey_scale,self.kernel,self.processed)
        
        contours=trait_image.find_contour(self.processed)

        self.final=orig
        box=trait_image.draw_contours(contours)
        
        angle=box[2]
        
        mon_fichier = open("fichier.txt", "r")
        first_angle=trait_image.arrondi(mon_fichier.read())
        mon_fichier.close
        
        angle=angle-first_angle
        sql = """\
        SELECT * FROM positions
        WHERE enfant_id = """+str(cdb.enfant_id)
        db=cdb.select_db(sql)[0]
        if angle <-90 or angle >90:
            print("ERROR: TOO FANTASTIC ANGLE")
        else:
       
            mon_fichier = open("previous_angle.txt", "r")
            previous_angle=trait_image.arrondi(mon_fichier.read())
            mon_fichier.close
            if abs(angle-previous_angle)<50:
                mon_fichier = open("previous_angle.txt", "w")
                mon_fichier.write(str(angle))
                mon_fichier.close()

                mon_fichier = open("angle_moteur.txt", "w")
                mon_fichier.write(str(angle))
                mon_fichier.close()
               
                
                print("OVALE2 ANGLE: "+str(int(angle)))
                if angle>=-90 and angle<-45:
                    zone="secteur1"
                elif angle>=-45 and angle<-10:
                    zone="secteur2"
                elif angle>=-10 and angle<10:
                    zone="secteur3"
                elif angle>=10 and angle<45:
                    zone="secteur4"
                elif angle>=45 and angle<90:
                    zone="secteur5"
                else:
                    print("ERROR")
                    
                    
                ##
                #On regarde depuis combien de temps le bébé est dans cette 
                #position, on met à jour la bdd, puis on anaslyse la 
                #bdd afin de savoir si il faut bouger le bébé
                ##
                timer=str(db['Date_mesure'])
                timer = datetime(int(timer[0]+timer[1]+timer[2]+timer[3]),int(timer[5]+timer[6]),int(timer[8]+timer[9]),int(timer[11]+timer[12]),int(timer[14]+timer[15]),int(timer[17]+timer[18]))
                timer=datetime.now()-timer
                timer=float(str(timer)[5:])+db[zone]
                cdb.update_db('positions',zone,timer)
                cdb.update_db('positions','Date_mesure','CURRENT_TIMESTAMP')


                
            else:
                print("ERROR TOO FAST")

    



