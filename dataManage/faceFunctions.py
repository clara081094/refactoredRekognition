from dataManage.drivers.sqliteFunctions import SqliteManage
from datetime import timedelta
import datetime
import base64
import json

'''CREATE TABLE t_faces (
	id_face INTEGER PRIMARY KEY AUTOINCREMENT,
	code_face TEXT NOT NULL,
	name_face TEXT,
	type_face TEXT,
	register_date_face DATETIME,
	caracteristics_face JSON );'''

class FaceFunctions:

    @staticmethod
    def getFacedRegistered(codeFace):
        t = (codeFace,)
        sql='''SELECT t1.id_face,t1.type_face FROM t_faces t1 where t1.code_face=?'''

        #print("resultado: "+SqliteManage().getFirstRow(sql,t))
        try:
            firstRow = SqliteManage().getFirstRow(sql,t)
            return firstRow[0],firstRow[1]
        except:
            return firstRow,firstRow

    @staticmethod
    def isVisitRegistered(codeFace,camera,dateTimes):

        t = (codeFace,dateTimes,camera)
        sql=''' SELECT t2.* 
                FROM t_visits t1
                    INNER JOIN t_faces t2 ON t1.id_face = t2.id_face
                WHERE t2.code_face=? AND date(t1.date_visit)=? AND t1.camara_visit=? '''

        return SqliteManage().hasRows(sql,t)

    @staticmethod
    def addFace(codeFace,nameFace,typeFace,dateTimes,caracteristics):

        t=(codeFace,nameFace,typeFace,dateTimes,json.dumps(caracteristics))
        sql='''INSERT INTO t_faces(
                code_face,
                name_face,
                type_face,
                register_date_face,
                caracteristics_face
                ) VALUES (?,?,?,?,?)'''
    
        SqliteManage().addRow(sql,t)
    
    @staticmethod
    def updateFace(typeFace,idFace):

        t=(typeFace,idFace,)
        sql=''' UPDATE t_faces 
                SET type_face = ?
                WHERE id_face = ?'''
        SqliteManage().addRow(sql,t)
        

    @staticmethod
    def addRegister(codeFace,nameFace,caracteristics,camera,frame,dateTimes,typeFace):

        idFace,type_name = FaceFunctions.getFacedRegistered(codeFace)
        if not idFace:
            FaceFunctions.addFace(codeFace,nameFace,typeFace,dateTimes,caracteristics)
            idFace,type_name = FaceFunctions.getFacedRegistered(codeFace)
        else:
            if type_name=='NUEVO':
                updateFace(typeFace,idFace)
            
        t=(dateTimes,idFace,json.dumps(caracteristics),frame,camera)
        sql='''INSERT INTO t_visits(
                    date_visit,
                    id_face,
                    caracteristics_visit,
                    frame_visit,
                    camara_visit
                    ) values (?,?,?,?,?)'''
        SqliteManage().addRow(sql,t)

    @staticmethod
    def getVisits(dateTimes,camera):

        t = (dateTimes,camera)
        sql=''' SELECT 
                    t2.code_face,
                    t2.type_face,
                    t2.caracteristics_face,
                    t1.caracteristics_visit,
                    t1.date_visit,
                    t1.camara_visit,
                    t1.frame_visit,
                    t2.name_face
                FROM t_visits t1
                    INNER JOIN t_faces t2 ON t1.id_face = t2.id_face
                WHERE 
                    date(t1.date_visit)=? AND
                    t1.camara_visit=?'''

        rows=SqliteManage().getRows(sql,t)
        result = []
        for row in rows :
            result.append({
                "code_face":row[0],
                "type_face":row[1],
                "caracteristics_face":row[2],
                "caracteristics_visit":row[3],
                "date_visit":row[4],
                "camara_visit":row[5],
                "frame_visit":row[6],
                "name_face":row[7]
            })

        return result

    @staticmethod
    def getVisitsByDate(self,dateTimes):

        t = (dateTimes)
        sql=''' SELECT 
                    t2.code_face,
                    t2.type_face,
                    t2.caracteristics_face,
                    t1.caracteristics_visit,
                    t1.date_visit,
                    t1.camara_visit,
                    t1.frame_visit
                FROM t_visits t1
                    INNER JOIN t_faces t2 ON t1.id_face = t2.id_face
                WHERE 
                    date(t1.date_visit)=?'''

        rows=SqliteManage().getRows(sql,t)
        result = []
        for row in rows :
            result.append({
                "code_face":row[0],
                "type_face":row[1],
                "caracteristics_face":row[2],
                "caracteristics_visit":row[3],
                "date_visit":row[4],
                "camara_visit":row[5],
                "frame_visit":row[6]
            })

        return result

    @staticmethod
    def getByFaceId(self,FaceId,cursor,connection):
        return 'bye'

    @staticmethod
    def truncate_table(self,cursor,connection):
        self.cursor.execute('''DELETE FROM REGISTRO''')
        self.connection.commit()
        self.conn.close()
