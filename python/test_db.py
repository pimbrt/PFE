#!/usr/bin/env python
#-*- coding: utf-8-*

import MySQLdb

# On créé un dictionnaire contenant les paramètres de connexion MySQL
paramMysql = {
    'host'   : 'localhost',
    'user'   : 'root',
    'passwd' : 'root',
    'db'     : 'test_db'
}

sql = """\
INSERT INTO people
(nom)
VALUES ('DROUET')
"""

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

finally:
    # On ferme la connexion
    if conn:
        conn.close()

'''
Le code précédent est utile mais seulement pour INSERT UPDATE et DELETE concernant SELECT le prochain fonctionne :
sql = """\
SELECT * FROM matable
WHERE monchamp1 = 'valeur1'
"""

try:
    # On  créé une conexion MySQL
    conn = MySQLdb.connect(**paramMysql)
    # On créé un curseur MySQL
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    # On exécute la requête SQL
    cur.execute(sql)
    # On récupère toutes les lignes du résultat de la requête
    rows = cur.fetchall()
    # On parcourt toutes les lignes
    for row in rows:
        # Pour récupérer les différentes valeurs des différents champs
        valeur1 = row['monchamp1']
        valeur2 = row['monchamp2']
        valeur3 = row['monchamp3']
        # etc etc ...

except MySQLdb.Error, e:
    # En cas d'anomalie
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)

finally:
    # On ferme la connexion
    if conn:
        conn.close()

'''
