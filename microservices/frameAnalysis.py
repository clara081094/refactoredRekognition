import json
import os
import base64
import cv2
import datetime
from library.rekognition import Rekognition
from datetime import timedelta
from dataManage.faceFunctions import FaceFunctions

class FrameAnalysis(object):

    generalPath = "/home/ubuntu/proyectos/microservicePlatanitos/pictures/"
    collection = "noConocidos"

    def cropImage(self,Width,Height,Left,Top,bytess,frame,count,camera):
    
        path=self.generalPath+str(camera)+"/faces/"

        fh = open(path+'imagetosave.jpg','wb')
        fh.write(bytess)
        fh.close()

        img = cv2.imread(path+'imagetosave.jpg')

        y, x, channels = img.shape

        w=int(float(x)*float(Width))
        h=int(float(y)*float(Height))
        l=int(float(x)*float(Left))
        t=int(float(y)*float(Top))

        if w<int(0) or h<int(0) or l<int(0) or t<int(0) :
            return None,None

        if l-2>=0 :
            crop_img = img[t:(t+h),l-2:(l+w+8)]
        else :
            crop_img = img[t:(t+h),l:(l+w+8)]

        nameFile = 'cara'+str(count)+'-'+str(frame)
        cv2.imwrite(path+nameFile, crop_img)
        img2 = cv2.imread(path+nameFile)

        with open(path+nameFile, 'rb') as image:
                free = bytearray(image.read())
        
        os.remove(path+'imagetosave.jpg')
        print("nameFile: ",nameFile)
        os.remove(path+nameFile)
        
        return free,nameFile

    def process(self,parameter):

        print("DETECTING FACES: ")

        dataBytes = parameter['dataBytes']
        frame = parameter['frame']
        camara = parameter['camara']

        backToBytes = base64.b64decode(dataBytes)
        response = Rekognition().detect_faces(backToBytes)

        if len(response['FaceDetails']) > 0 :

            count = 1

            for record in response['FaceDetails']: 
                bad = 0
                coordenate = record['BoundingBox']
                personalImage, nameImage = self.cropImage(coordenate['Width'],coordenate['Height'],coordenate['Left'],coordenate['Top'],backToBytes,frame,count,camara)
                
                if float(record['Confidence'])  >= 80 and personalImage: 
                    dateToday = (datetime.datetime.now()-timedelta(hours=5))
                    rp = Rekognition().face_recog(personalImage,self.collection)
                    
                    if rp == "BAD":
                        bad = 1
                    else:
                        rpta = rp['FaceMatches']

                    if bad == 0 and len(rpta) != 0:

                        codeFace = rpta[0]['Face']['FaceId']

                        if FaceFunctions().isVisitRegistered(codeFace,camara,dateToday.date()):
                            print("Ya se registo en bd paso de recurrente")
                        else: 
                            print("Registrar en bd paso de recurrente")
                            nameFace=""
                            FaceFunctions().addRegister(codeFace,nameFace,record,camara,frame,dateToday,"RECURRENTE")

                    else:

                        if bad == 0 :
                            
                            print("Nueva persona")
                            nameFace = "Registrado-dia-" + str(dateToday.time())
                            rpta3 = Rekognition().index_faces(personalImage,self.collection,nameImage)

                            if rpta3 == "BAD":
                                print("Error en registrar la nueva face")
                                bad=1

                            if bad == 0:
                                codeFace=rpta3['FaceRecords'][0]['Face']['FaceId']
                                path=self.generalPath+str(camara)+"/registered/"
                                fh = open(path+faceId+".jpg",'wb')
                                fh.write(personalImage)
                                fh.close()

                                FaceFunctions().addRegister(codeFace,nameFace,record,camara,frame,dateToday,"NUEVO")
                                    
                count = count + 1

