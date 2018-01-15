#!/usr/bin/python3.6
# -*-coding:Latin-1 -*

import MySQLdb
from datetime import datetime
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
    def __init__(self,angle,first_pic_or_second):
        if first_pic_or_second==1:
            #changer la date seulement
            self.update_db('positions','Date_mesure','CURRENT_TIMESTAMP') 
            print("done")
            print("stop")
        else:
            db=self.select_db('*','positions')#timer [0  2 ?]
            timer=db[0]['Date_mesure']
            if angle>=0 and angle<45:
                zone="secteur1"
            elif angle>=45 and angle<80:
                zone="secteur2"
            elif angle>=80 and angle<100:
                zone="secteur3"
            elif angle>=100 and angle<135:
                zone="secteur4"
            elif angle>=135 and angle<180:
                zone="secteur5"
            else:
                print("ERROR")
            #ici time=actualtime-oldtime
            timer = str(timer)
            timer = datetime(int(timer[0]+timer[1]+timer[2]+timer[3]),int(timer[5]+timer[6]),int(timer[8]+timer[9]),int(timer[11]+timer[12]),int(timer[14]+timer[15]),int(timer[17]+timer[18]))
            timer=datetime.now()-timer
            timer=timer.seconds+db[0][zone]
            
            self.update_db('positions',zone,timer)
        
        
    def update_db(self,fraum,zone,timer):
        #ajouter zone lÃ 
        sql = """\
        UPDATE `"""+str(fraum)+"""` SET `"""+str(zone)+"""`="""+str(timer)+""",  `Date_mesure`=CURRENT_TIMESTAMP WHERE  `enfant_id` = """+str(enfant_id)+""" """
        print(sql)
        self.send_to_db(sql)
    def select_db(self,what,fraum):
        sql = """\
        SELECT """+str(what)+""" FROM """+str(fraum)+"""
        WHERE enfant_id = """+str(enfant_id)
        
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
            
        
        #finally:
            # On ferme la connexion
            #if conn:
             #   conn.close()

             
#import time    
#time.strftime('%Y-%m-%d %H:%M:%S')
