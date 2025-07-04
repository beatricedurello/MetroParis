from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.fermata import Fermata


class DAO():

    @staticmethod
    def getAllFermate():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM fermata"
        cursor.execute(query)

        for row in cursor:
            result.append(Fermata(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def hasConnessione(u,v):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = ("SELECT * FROM connessione c WHERE c.id_stazP = %s and c.id_stazA = %s")
        cursor.execute(query, (u.id_fermata,v.id_fermata))

        for row in cursor:
            result.append(row)
        cursor.close()
        conn.close()
        return len(result)>0

    @staticmethod
    def getVicini(u: Fermata):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = ("SELECT * "
                 "FROM connessione c "
                 "WHERE c.id_stazP = %s")
        cursor.execute(query, (u.id_fermata,))

        for row in cursor:
            result.append(Connessione(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = ("SELECT * "
                 "FROM connessione c ")
        cursor.execute(query)

        for row in cursor:
            result.append(Connessione(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesPesati():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = ("SELECT id_stazP, id_stazA, COUNT(*) as n "
                 "FROM connessione c "
                 "GROUP BY id_stazP, id_stazA "
                 "ORDER BY n DESC ")
        cursor.execute(query)

        for row in cursor:
            result.append((row['id_stazP'], row['id_stazA'], row['n']))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesVelocita():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = ("SELECT c.id_stazP, c.id_stazA, max(l.velocita) as v "
                 "FROM connessione c, linea l "
                 "WHERE c.id_linea = l.id_linea "
                 "GROUP BY id_stazP, id_stazA "
                 "ORDER BY id_stazP desc, id_stazA desc")
        cursor.execute(query)

        for row in cursor:
            result.append((row['id_stazP'], row['id_stazA'], row['v']))
        cursor.close()
        conn.close()
        return result
