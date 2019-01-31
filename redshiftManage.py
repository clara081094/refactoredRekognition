import datetime
from datetime import timedelta
import psycopg2

'''CREATE TABLE IF NOT EXISTS public.face
(
	face_code VARCHAR(256) NOT NULL  ENCODE lzo
	,face_name VARCHAR(90)   ENCODE lzo
	,face_place VARCHAR(256)   ENCODE lzo
	,face_date TIMESTAMP WITHOUT TIME ZONE NOT NULL  ENCODE lzo
	,face_averageage SMALLINT   ENCODE lzo
	,face_ishappy BOOLEAN   ENCODE RAW
	,face_issad BOOLEAN   ENCODE RAW
	,face_isangry BOOLEAN   ENCODE RAW
	,face_isconfused BOOLEAN   ENCODE RAW
	,face_isdisgusted BOOLEAN   ENCODE RAW
	,face_issurprised BOOLEAN   ENCODE RAW
	,face_id BIGINT   ENCODE lzo
	,face_gender 
)
DISTSTYLE EVEN;'''

import json 

class RedshiftManage(object):

    def __init__(self):
        self.conn = psycopg2.connect(
            dbname='main', 
            host='super-jupiter.cbxz5zw04qfi.us-east-1.redshift.amazonaws.com', 
            port='5439',
            user='root', 
            password='eV132!629MiK')
        self.cursor = self.conn.cursor()
        #print(self.cursor)

    def add_register(self,faceId,dateFace,place,grop):

        group = json.loads(grop)

        face_code = faceId
        face_name = group['name']
        try:
            face_type = group['tipo']
        except:
            face_type = ""
        face_place = place
        face_date = dateFace
        face_averageage = (int(group['extra']['AgeRange']['High'])+int(group['extra']['AgeRange']['Low']))/2
        face_gender = group['extra']['Gender']['Value']

        #print(face_code,",",face_name,",",face_place,",",face_date,",",face_averageage,",",face_gender)
        face_isHappy=False
        face_isAngry=False
        face_isConfused=False
        face_isSurprised=False
        face_isCalm=False
        face_isDisgusted=False
        face_isSad=False

        for emotion in group['extra']['Emotions']:
            if float(emotion['Confidence']) >= 70 :
                print("Number")
                if emotion['Type'] == "HAPPY" :
                    face_isHappy=True
                if emotion['Type'] == "ANGRY" :
                    face_isAngry=True
                if emotion['Type'] == "CONFUSED" :
                    face_isConfused=True
                if emotion['Type'] == "SURPRISED" :
                    face_isSurprised=True
                if emotion['Type'] == "CALM" :
                    face_isCalm=True
                if emotion['Type'] == "DISGUSTED" :
                    face_isDisgusted=True
                if emotion['Type'] == "SAD" :
                    face_isSad=True


        registro = (face_code,face_name,face_place,face_date,face_averageage,face_gender,face_isHappy,face_isSad,face_isAngry,
        face_isConfused,face_isDisgusted,face_isSurprised,face_isCalm,face_type)
        sql = '''INSERT INTO main.faces(
            face_code
            ,face_name
            ,face_place
            ,face_date
            ,face_averageage
            ,face_gender
            ,face_ishappy
            ,face_issad
            ,face_isangry
            ,face_isconfused
            ,face_isdisgusted
            ,face_issurprised
            ,face_iscalm
            ,face_type
             ) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''

        self.cursor.execute(sql, registro)
        self.conn.commit()
        self.conn.close()

    def prueba(self):
        sql = '''INSERT INTO faces(face_code) values ('codigo123')'''
        self.conn.close()
