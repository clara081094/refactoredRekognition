from dataManage import DataManage
import json 

class ReportAnalysis(object):

    def get_Emotions(self,caracteristics):

        emotions = [] 
        for emotion in caracteristics['Emotions']:
            if float(emotion['Confidence']) >= 70 :
                emotions.append(emotion['Type'])
        
        return emotions


    def day_Report(self,parameter):

        dia=parameter['dia']
        camara=parameter['camara']
        rowsKnown = DataManage().obtain_rows(0,dia,camara)
        rowsStranger = DataManage().obtain_rows(1,dia,camara)

        lenrk=len(rowsKnown)
        lenrs=len(rowsStranger)

        if lenrk == 0 and lenrs == 0 :
            message = { "data":{},"message":"No hay registros"}
        else:
            conocidos = {}
            desconocidos = {}
            if lenrk > 0:
                conocidos = {"cantidad":lenrk}
                listaConocidos = []
                for record in rowsKnown :
                    try:
                        tipo=json.loads(record['caracteristicas'])['tipo']
                    except:
                        tipo=""
                    salida = {
                        "faceId":record['faceId'],
                        "tipo":tipo,
                        "nombre":json.loads(record['caracteristicas'])['name'],
                        "frame":record['frame'],
                        "fecha":record['fecha'],
                        "genero":json.loads(record['caracteristicas'])['extra']['Gender']['Value'],
                        "edad":(int(json.loads(record['caracteristicas'])['extra']['AgeRange']['High'])+
                        int(json.loads(record['caracteristicas'])['extra']['AgeRange']['Low']))/2,
                        "emociones":self.get_Emotions(json.loads(record['caracteristicas'])['extra'])
                    }
                    listaConocidos.append(salida)
                conocidos.update({"personas":listaConocidos})
            if lenrs > 0:
                desconocidos = { "cantidad":lenrs }
                listaDesconocidos = []
                for record in rowsStranger :
                    try:
                        tipo=json.loads(record['caracteristicas'])['tipo']
                    except:
                        tipo=""
                    salida = {
                        "faceId":record['faceId'],
                        "nombre":json.loads(record['caracteristicas'])['name'],
                        "tipo":tipo,
                        "frame":record['frame'],
                        "fecha":record['fecha'],
                        "genero":json.loads(record['caracteristicas'])['extra']['Gender']['Value'],
                        "edad":(int(json.loads(record['caracteristicas'])['extra']['AgeRange']['High'])+
                        int(json.loads(record['caracteristicas'])['extra']['AgeRange']['Low']))/2,
                        "emociones":self.get_Emotions(json.loads(record['caracteristicas'])['extra'])
                    }
                    listaDesconocidos.append(salida)
                desconocidos.update({"personas":listaDesconocidos})
            message = { "data":{ "conocidos": conocidos, "desconocidos": desconocidos },"message":"Hay registros"}
        return message


            

