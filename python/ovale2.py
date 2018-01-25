#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import pic
import trait_image
from datetime import datetime
#si marche pas changer ' par `
# On crÃ©Ã© un dictionnaire contenant les paramÃ¨tres de connexion MySQL
paramMysql = {
    'host'   : 'localhost',
    'user'   : 'root',
    'passwd' : 'root',
    'db'     : 'raphy_pfe'
}

#un enfant = une raspberry donc dans la base de données l'enfant sera le numéro 1
enfant_id = 1 

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
        WHERE enfant_id = """+str(enfant_id)
        db=self.select_db(sql)[0]
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
                timer=timer.seconds+db[zone]
                self.update_db('positions',zone,timer)

                
            else:
                print("ERROR TOO FAST")

    
    def update_db(self,fraum,zone,timer):
        #ajouter zone lÃ 
        sql = """\
        UPDATE """+str(fraum)+""" SET """+str(zone)+"""="""+str(timer)+""" 
        WHERE  enfant_id = """+str(enfant_id)
        self.send_to_db(sql)
        
    def select_db(self,sql):
        
        try:
            # On  créé une conexion MySQL
            conn = MySQLdb.connect(**paramMysql)
            # On créé un curseur MySQL
            cur = conn.cursor(MySQLdb.cursors.DictCursor)
            # On exécute la requÃªte SQL
            cur.execute(sql)
            # On récupère toutes les lignes du résultat de la requête
            rows = cur.fetchall()
            return rows
        except MySQLdb.Error, e:
            # En cas d'anomalie
            print "Error %d: %s" % (e.args[0],e.args[1])
         
        

    def send_to_db(self,sql):

        try:
            # On  créé une conexion MySQL
            conn = MySQLdb.connect(**paramMysql)
            # On créé un curseur MySQL
            cur = conn.cursor()
            try:
                # On exécute la requête SQL
                cur.execute(sql)
                # On commit
                conn.commit()
            except MySQLdb.Error, e:
                # En cas d'erreur on annule les modifications
                conn.rollback()
        
        except MySQLdb.Error, e:
            # En cas d'anomalie
            print "Error %d: %s" % (e.args[0],e.args[1])
            
            
        



