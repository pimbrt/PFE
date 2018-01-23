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

enfant_id = 1 


class database:
    def __init__(self,angle,length,ODL,ODR,first_pic_or_second):
        if first_pic_or_second==1:
            #changer la date seulement
            #si ça mache pas il faut créer la ligne avant
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
                    #ici time=actualtime-oldtime
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
        db=self.select_db("*","positions")[0]
        secteur={"-67":int(db['secteur1']),"-22":int(db['secteur2']),"0":int(db['secteur3']),"22":int(db['secteur4']),'67':int(db['secteur5'])}
        #minimum=int(min(secteur.items(), key=lambda x: x[1]) [0])
        #mini=secteur["-67"]
        #mini_key="-67"
       # for key in secteur:
        #    if mini> secteur[key]:
         #       mini = secteur[key]
          #      mini_key=key
        #maxi=secteur["-67"]
        #maxi_key="-67"
        #for key in secteur:
         #   if maxi> secteur[key]:
          #      maxi = secteur[key]
           #     maxi_key=key 
        #print (minimum,angle)
        array={"left":secteur["-67"]+secteur["-22"],
        "right":secteur["67"]+secteur["22"],
        "middle":secteur["0"]}
        mini=array["left"]
        mini_key="left"
        for key in array:
            if mini> array[key]:
                mini = array[key]
                mini_key=key
        maxi=array["right"]
        maxi_key="right"
        for key in array:
            if maxi< array[key]:
                maxi = array[key]
                maxi_key=key

                
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
        print("KEY")
        print(array[maxi_key],array[mini_key])
        
        if array[maxi_key]-array[mini_key]>ecart and key!= zone_num :  
            print("ACTION VALIDATED")
            tm.moveMotors(int(key),angle)
        #finally:
            # On ferme la connexion
            #if conn:
             #   conn.close()

