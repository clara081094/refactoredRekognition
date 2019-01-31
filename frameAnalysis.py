import json
import os
import base64
import cv2
import datetime
from rekognition import Rekognition
from datetime import timedelta
from dataManage import DataManage

class FrameAnalysis(object):

    def cropImage(self,Width,Height,Left,Top,bytess,frame,count,camera):
    
        path="/home/ubuntu/proyectos/microservicePlatanitos/pictures/"+str(camera)+"/faces/"

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

            #print("response2:")
            #print(response2)
            count = 1

            for record in response['FaceDetails']: 
                bad = 0
                #face = record['Face']
                #print("Face detail confidence: ",record)
                coordenate = record['BoundingBox']
                personalImage, nameImage = self.cropImage(coordenate['Width'],coordenate['Height'],coordenate['Left'],coordenate['Top'],backToBytes,frame,count,camara)
                
                if float(record['Confidence'])  >= 80 and personalImage: 
                    rp = Rekognition().face_recog(personalImage,"noConocidos")
                    
                    if rp == "BAD":
                        bad = 1
                    else:
                        rpta = rp['FaceMatches']

                    if bad == 0 and len(rpta) != 0:
                        #print("SE DETECTO  A UN RECONOCIDO: ",rpta[0]['Face'])
                        if(DataManage().isRegistered(rpta[0]['Face']['FaceId'],1,camara)):
                            print("Ya se registo paso de no conocido")
                        else: 
                            print("Registrar paso de no conocido")
                            nameId = "Extraño-" + str((datetime.datetime.now()-timedelta(hours=5)).time())
                            caracteristicas = { "name":nameId ,"extra": record ,"tipo":"recurrente" }
                            DataManage().add_register(rpta[0]['Face']['FaceId'],caracteristicas,1,camara,nameImage)
                    else:

                        if bad == 0 :
                            rp2=Rekognition().face_recog(personalImage,"rekVideoBlog")
                            
                            if rp2 == "BAD":
                                bad = 1
                            else:
                                rpta2 = rp2['FaceMatches']

                        if bad == 0 and len(rpta2) != 0:

                            if(DataManage().isRegistered(rpta2[0]['Face']['FaceId'],0,camara)):
                                print("Ya se registo paso de conocido")
                            else:
                                print("Registrar paso de conocido")
                                caracteristicas = {"name":rpta[0]['Face']['ExternalImageId'],"extra":record,"tipo":"conocido"}
                                DataManage().add_register(rpta2[0]['Face']['FaceId'],caracteristicas,0,camara,nameImage)
                        else:

                            if bad == 0:
                                print("Nueva persona")
                                nameId = "Extraño-" + str((datetime.datetime.now()-timedelta(hours=5)).time())
                                caracteristicas = { "name":nameId ,"extra": record,"tipo":"nuevo"}
                                rpta3 = Rekognition().index_faces(personalImage,"noConocidos",nameImage)

                                if rpta3 == "BAD":
                                    print("Error en registrar la nueva face")
                                    bad=1

                                if bad == 0:
                                    faceId=rpta3['FaceRecords'][0]['Face']['FaceId']
                                    path="/home/ubuntu/proyectos/microservicePlatanitos/pictures/"+str(camara)+"/registered/"
                                    fh = open(path+faceId+".jpg",'wb')
                                    fh.write(personalImage)
                                    fh.close()

                                    DataManage().add_register(faceId,caracteristicas,1,camara,nameImage)
                                    

                            

                count = count + 1

