#!/usr/bin/python3.6
# -*-coding:Latin-1 -*

#import MySQLdb

# On créé un dictionnaire contenant les paramètres de connexion MySQL
paramMysql = {
    'host'   : 'localhost',
    'user'   : 'root',
    'passwd' : 'root',
    'db'     : 'test_db'
}


class database:
    def __init__(self,angle):
        if angle>=0 and angle<45:
            zone=1
        if angle>=45 and angle<80:
            zone=2
        if angle>=80 and angle<100:
            zone=3
        if angle>=100 and angle<135:
            zone=4
        if angle>=135 and angle<180:
            zone=5
        
        self.insert_to_sql(zone)
    def insert_to_sql(self,zone):
        #ajouter zone là
        sql = """\
        INSERT INTO people
        (nom)
        VALUES ('DROUET')
        """
        self.send_to_db(sql)

    def send_to_db(self,sql):
        print("plus tard")
        '''
        On va faire comme si on obtenait correctement box, du coup on connait l'angle
        box=90+box
        on prend le temps d'aujourd'hui on suppose que depuis la derniere prise il n y a pas eu de mouvemebt resultat on selecte les bonnes infos dans la bdd et on additionne en parler à edouard ça serait plus simple que le laisser tout additionner
        '''''''
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
            sys.exit(1)
        
        #finally:
            # On ferme la connexion
            #if conn:
             #   conn.close()
        '''