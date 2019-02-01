from dataManage.faceFunctions import FaceFunctions
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

        rows = FaceFunctions().getVisits(dia,camara)

        if len(rowsKnown) == 0:
            message = { "data":{},"message":"No hay registros"}
        else:
            listaTrabajadores:[]
            listaRecurrentes:[]
            listaNuevos:[]

            for record in rows:
                
                salida = {
                        "codeFace":record['code_face'],
                        "tipo":record['type_face'],
                        "nombre":record['name_face'],
                        "frame":record['frame_visit'],
                        "fecha":record['date_visit'],
                        "genero":json.loads(record['caracteristics_face'])['Gender']['Value'],
                        "edad":(int(json.loads(record['caracteristics_face'])['AgeRange']['High'])+
                        int(json.loads(record['caracteristics_face'])['AgeRange']['Low']))/2,
                        "emociones":self.get_Emotions(json.loads(record['caracteristics_face']))
                }

                if record['type_face']=='TRABAJADOR':
                    listaTrabajadores.append(salida)
                if record['type_face']=='NUEVO':
                    listaNuevos.append(salida)
                if record['type_face']=='RECURRENTE':
                    listaRecurrentes.append(salida)

            respuesta = {
                "Trabajadores":{
                    "cantidad":len(listaTrabajadores),
                    "personas":listaTrabajadores
                },
                "Nuevos":{
                    "cantidad":les(listaNuevos),
                    "personas":listaNuevos
                },
                "Recurrentes":{
                    "cantidad":les(listaRecurrentes),
                    "personas":listaRecurrentes
                },
            }

            message = { "data": respuesta ,"message":"Hay registros"}

        return message


            

