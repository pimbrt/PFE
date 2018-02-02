#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import MySQLdb
# On crÃ©Ã© un dictionnaire contenant les paramÃ¨tres de connexion MySQL
paramMysql = {
    'host'   : 'localhost',
    'user'   : 'root',
    'passwd' : 'root',
    'db'     : 'raphy_pfe'
}

#un enfant = une raspberry donc dans la base de données l'enfant sera le numéro 1
enfant_id = 1
def send_to_db(sql):

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


def update_db(fraum,zone,timer):
    #ajouter zone lÃ 
    sql = """\
    UPDATE """+str(fraum)+""" SET """+str(zone)+"""="""+str(timer)+""" 
    WHERE  enfant_id = """+str(enfant_id)
    send_to_db(sql)
        
def select_db(sql):
        
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
         
