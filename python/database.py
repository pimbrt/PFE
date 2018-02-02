#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import MySQLdb
from datetime import datetime
from math import frexp
import main_moteur as mm
import trait_image
import conn_db as cdb


class database:
    def __init__(self,angle,length,ODL,ODR,first_pic_or_second):
        ##
        #Si la photo est la premiere analysée on enregistre ODL ODR largeur et 
        #longueur puis previous angle afin d'avoir l'angle précédent 
        #(pour la prochaine analyse, oprevious angle n'est pas utile si on 
        #est dans le noir mais par sécu on garde)
        ##
        if first_pic_or_second==1:
            longueur=length[0]
            largeur=length[1]
            
            sql = """\
            UPDATE `datas` SET `largeur`="""+str(largeur)+""", `longueur`="""+str(longueur)+""", 
            `ODL`="""+str(ODL)+""", `ODR`="""+str(ODR)+""", `date_data`=CURRENT_TIMESTAMP WHERE  enfant_id = """+str(cdb.enfant_id)
            print("SQL : "+str(sql))
            cdb.send_to_db(sql)
            
            cdb.update_db('positions','Date_mesure','CURRENT_TIMESTAMP')
           
            mon_fichier = open("previous_angle.txt", "w")
            mon_fichier.write(str(angle))
            mon_fichier.close()
        ##
        #Si la photo analysée n'est pas la première on regarde si l'angle 
        #trouvé est abérrant par rapport au précédent et à -90 90
        #Puis en fonction de l'angle trouvé on lui attribue une zone et on 
        #donne à zone_num l'angle nà atteindre pour être dans cette zone sert
        #un peu plus bas on enregistre dans timer la date de la dernière mesure
        #select_db selectionne la ligne de la base de données où la position 
        #du bébé a été enregistrée en continue (pour chaque zone on a un temps 
        #en seconde)
        ##
        else:
            
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


                    print("*******ANGLE: "+str(int(angle)))
                    if angle>=-90 and angle<-45:
                        zone="secteur1"
                        zone_num="-50"
                    elif angle>=-45 and angle<-10:
                        zone="secteur2"
                        zone_num="-22"
                    elif angle>=-10 and angle<10:
                        zone="secteur3"
                        zone_num="0"
                    elif angle>=10 and angle<45:
                        zone="secteur4"
                        zone_num="22"
                    elif angle>=45 and angle<90:
                        zone="secteur5"
                        zone_num="50"
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
                    print("YES ANALYSE ...")
                    self.analyse(angle,zone_num,db)
                else:
                    print("ERROR: TOO FAST")

    def analyse(self,angle,zone_num,db):       
        
        #On les enregistre dans ce dico
        secteur={"-50":int(db['secteur1']),"-22":int(db['secteur2']),
                 "0":int(db['secteur3']),"22":int(db['secteur4']),
                 '50':int(db['secteur5'])}

        # dans array on calcule le temps passé à gauche et à droite
        array={"left":secteur["-50"]+secteur["-22"],
        "right":secteur["50"]+secteur["22"],
        "middle":secteur["0"]}
        #On cherche dans array la zone la moins sollicité
        mini=array["left"]
        mini_key="left"
        for key in array:
            if mini> array[key]:
                mini = array[key]
                mini_key=key
        #On cherche dans array la zone la plus sollicitée
        maxi=array["right"]
        maxi_key="right"
        for key in array:
            if maxi< array[key]:
                maxi = array[key]
                maxi_key=key

        #on cherche dans la zone la moins sollicitée la tranche la moins sollicité
        if mini_key=="left":
            if secteur["-50"]>secteur["-22"]:
                key="-22"
            else:
                key="-50"
        elif mini_key=="right":
            if secteur["50"]>secteur["22"]:
                key="22"
            else:
                key="50"
        else:
            key="0"
            
        

        # si l'écart en secondes entre la zone la moins sollicitée et la plus 
        #est supérieur à la variable écart et que l'enfant n'est pas dans la 
        #zone la moins sollicitée on demande aux moteurs d'obtenir l'angle 
        #correspondant à la tranche la moins sollicitée de la zone la moins 
        #sollicitée les moteurs vont donc alors (en vérifiant l'angle obtenu au
        #fur et à mesure) déplacer l'enfant jusqu'à obtenir un angle convaincant
        sql = """\
            SELECT * FROM datas
            WHERE enfant_id = """+str(cdb.enfant_id)
        db=cdb.select_db(sql)[0]

        ecart=5
        
        if array[maxi_key]-array[mini_key]>ecart and key!= zone_num and db['alert']==0:  
            print("ACTION VALIDATED")
            self.save_action()
            mm.moveMotors(int(key),angle)
            
    def save_action(self):
        today=str(datetime.now())[0:10]
        sql = """\
        SELECT * FROM actions
        WHERE date = '"""+today+"""'
        """

        
        try :
            rows=cdb.select_db(sql)[0]
            nb_action=rows['nb_action']+1
            sql = """\
            UPDATE actions SET nb_action="""+str(nb_action)+""" WHERE  date = '"""+today+"""'"""
            cdb.send_to_db(sql)
        except IndexError :
            sql = """\
            INSERT INTO actions
            (`enfant_id`,`nb_action`,`date`)
            VALUES (1,1,CURRENT_TIMESTAMP)
            """
            cdb.send_to_db(sql)
#finally:
# On ferme la connexion
#if conn:
 #   conn.close()

