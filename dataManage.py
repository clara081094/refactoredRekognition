import datetime
from datetime import timedelta
import base64
import sqlite3, json
from redshiftManage import RedshiftManage


'''CREATE TABLE REGISTRO (
   ...> id integer PRIMARY KEY AUTOINCREMENT,
   ...> faceId TEXT NOT NULL,
   ...> caracteristicas JSON,
   ...> fecha DATETIME NOT NULL,
   ...> estado INTEGER NOT NULL,
   ...> camara TEXT NOT NULL,
   ...> frame TEXT NOT NULL );'''

class DataManage(object):

    def __init__(self):
        self.conn = sqlite3.connect('/home/ubuntu/proyectos/microservicePlatanitos/rekognition.db')
        self.cursor = self.conn.cursor()

    def isRegistered(self,FaceId,state,camara):
        timeCompare = datetime.datetime.now()-timedelta(hours=5)
        dayCompare = (datetime.datetime.now()-timedelta(hours=5)).date()
        t = (FaceId,state,dayCompare,camara)
        self.cursor.execute('''SELECT * FROM REGISTRO WHERE faceId=? AND estado=? AND date(fecha)=? AND camara=?''', t)

        if self.cursor.fetchone() :
            self.conn.close()
            return True
        else :
            self.conn.close()
            return False

    def add_register(self,faceId,caracteristicas,estado,camara,frame):

        tiempo = datetime.datetime.now()-timedelta(hours=5)

        registro = (faceId,json.dumps(caracteristicas),tiempo,estado,camara,frame)
        sql = '''INSERT INTO REGISTRO (faceId,caracteristicas,fecha,estado,camara,frame) values (?,?,?,?,?,?)'''
        self.cursor.execute(sql, registro)
        self.conn.commit()
        self.conn.close()

    def obtain_rows(self,state,fecha,camara):

        t = (state,datetime.datetime.strptime(fecha,"%d/%m/%Y").date(),camara)

        rows=self.cursor.execute('''SELECT faceId as 'faceId', caracteristicas as 'caracteristicas', fecha as 'fecha', 
        estado as 'estado',camara as 'camara', frame as 'frame' FROM REGISTRO WHERE estado=? AND date(fecha)=? AND camara=?''', t)
        result = []
        for row in rows :
            result.append({
                "faceId":row[0],
                "caracteristicas":row[1],
                "fecha":row[2],
                "estado":row[3],
                "camara":row[4],
                "frame":row[5]
            })

        self.conn.close()
        return result

    def obtain_rows_date(self,fecha):

        t = (fecha,)

        rows=self.cursor.execute('''SELECT faceId as 'faceId', caracteristicas as 'caracteristicas', fecha as 'fecha', 
        estado as 'estado',camara as 'camara', frame as 'frame' FROM REGISTRO WHERE date(fecha)=? ''', t)

        result = []
        for row in rows :
            result.append({
                "faceId":row[0],
                "caracteristicas":row[1],
                "fecha":row[2],
                "estado":row[3],
                "camara":row[4],
                "frame":row[5]
            })

        self.conn.close()
        return result

    def det_byId(self,FaceId,cursor,connection):
        return 'jais'

    def truncate_table(self,cursor,connection):
        self.cursor.execute('''DELETE FROM REGISTRO''')
        self.connection.commit()
        self.conn.close()
