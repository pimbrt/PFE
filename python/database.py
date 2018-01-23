#!/usr/bin/python3.6
# -*-coding:Latin-1 -*

import MySQLdb
from datetime import datetime
from math import frexp
import test_moteur as tm
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
            UPDATE `datas` SET `largeur`="""+str(largeur)+""", `longueur`="""+str(longueur)+""", `ODL`="""+str(ODL)+""", `ODR`="""+str(ODR)+""" WHERE  enfant_id = '"""+str(enfant_id)+"""'"""
            print("SQL : "+str(sql))
            self.send_to_db(sql)
            self.update_db('positions','Date_mesure','CURRENT_TIMESTAMP')
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
            db=self.select_db('*','positions')[0]#timer [0  2 ?]
            if angle <-90 or angle >90:
                print("ERROR: TOO FANTASTIC ANGLE")
            else:
       
                mon_fichier = open("previous_angle.txt", "r")
                previous_angle=self.arrondi(mon_fichier.read())
                mon_fichier.close
                if abs(angle-previous_angle)<50:
                    mon_fichier = open("previous_angle.txt", "w")
                    mon_fichier.write(str(angle))
                    mon_fichier.close()


                    print("*******ANGLE: "+str(int(angle)))
                    timer=str(db['Date_mesure'])
                    if angle>=-90 and angle<-45:
                        zone="secteur1"
                        zone_num="-67"
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
                        zone_num="67"
                    else:
                        print("ERROR")
                        
                        
                    ##
                    #On regarde depuis combien de temps le bébé est dans cette 
                    #position puis on met à jour la bdd, puis on anaslyse la 
                    #bdd afin de savoir si il faut bouger le bébé
                    ##
                    timer = datetime(int(timer[0]+timer[1]+timer[2]+timer[3]),int(timer[5]+timer[6]),int(timer[8]+timer[9]),int(timer[11]+timer[12]),int(timer[14]+timer[15]),int(timer[17]+timer[18]))
                    timer=datetime.now()-timer
                    timer=timer.seconds+db[zone]
                    self.update_db('positions',zone,timer)
                    print("YES ANALYSE ...")
                    self.analyse(angle,zone_num)
                else:
                    print("ERROR: TOO FAST")
                    
                
        
        
    def update_db(self,fraum,zone,timer):
        #ajouter zone lÃ 
        sql = """\
        UPDATE """+str(fraum)+""" SET """+str(zone)+"""="""+str(timer)+""" WHERE  enfant_id = '"""+str(enfant_id)+"""'
        """
        self.send_to_db(sql)
    def select_db(self,what,fraum):
        sql = """\
        SELECT """+str(what)+""" FROM """+str(fraum)+"""
        WHERE enfant_id = '"""+str(enfant_id)+"""'
        """
        
        try:
            # On  crÃ©Ã© une conexion MySQL
            conn = MySQLdb.connect(**paramMysql)
            # On crÃ©Ã© un curseur MySQL
            cur = conn.cursor(MySQLdb.cursors.DictCursor)
            # On exÃ©cute la requÃªte SQL
            cur.execute(sql)
            # On rÃ©cupÃ¨re toutes les lignes du rÃ©sultat de la requÃªte
            rows = cur.fetchall()
            # On parcourt toutes les lignes
            #for row in rows:
                # Pour rÃ©cupÃ©rer les diffÃ©rentes valeurs des diffÃ©rents champs
                #valeur1 = row['monchamp1']
                #valeur2 = row['monchamp2']
                #valeur3 = row['monchamp3']
                # etc etc ...
            
            return rows
        except MySQLdb.Error, e:
            # En cas d'anomalie
            print "Error %d: %s" % (e.args[0],e.args[1])
         
        

    def send_to_db(self,sql):

        try:
            # On  crÃ©Ã© une conexion MySQL
            conn = MySQLdb.connect(**paramMysql)
            # On crÃ©Ã© un curseur MySQL
            cur = conn.cursor()
            try:
                # On exÃ©cute la requÃªte SQL
                cur.execute(sql)
                # On commit
                conn.commit()
            except MySQLdb.Error, e:
                # En cas d'erreur on annule les modifications
                conn.rollback()
        
        except MySQLdb.Error, e:
            # En cas d'anomalie
            print "Error %d: %s" % (e.args[0],e.args[1])
    def arrondi(self,nb):
        nb=str(nb).split('.')
        if int(nb[1])>=5:
            return int(nb[0])+1
        else:
            return int(nb[0])


    def analyse(self,angle,zone_num):
        #On  cherche les habitudes du bébé
        db=self.select_db("*","positions")[0]
        
        #On les enregistre dans ce dico
        secteur={"-67":int(db['secteur1']),"-22":int(db['secteur2']),"0":int(db['secteur3']),"22":int(db['secteur4']),'67':int(db['secteur5'])}

        # dans array on calcule le temps passé à gauche et à droite
        array={"left":secteur["-67"]+secteur["-22"],
        "right":secteur["67"]+secteur["22"],
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
            if secteur["-67"]>secteur["-22"]:
                key="-22"
            else:
                key="-67"
        elif mini_key=="right":
            if secteur["67"]>secteur["22"]:
                key="22"
            else:
                key="67"
        else:
            key="0"
            
        ecart=5

        # si l'écart en secondes entre la zone la moins sollicitée et la plus 
        #est supérieur à la variable écart et que l'enfant n'est pas dans la 
        #zone la moins sollicitée on demande aux moteurs d'obtenir l'angle 
        #correspondant à la tranche la moins sollicitée de la zone la moins 
        #sollicitée les moteurs vont donc alors (en vérifiant l'angle obtenu au
        #fur et à mesure) déplacer l'enfant jusqu'à obtenir un angle convaincant
        if array[maxi_key]-array[mini_key]>ecart and key!= zone_num :  
            print("ACTION VALIDATED")
            tm.moveMotors(int(key),angle)
            
            
            
            
#finally:
# On ferme la connexion
#if conn:
 #   conn.close()

