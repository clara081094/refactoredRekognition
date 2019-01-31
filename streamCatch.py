# Program To Read video
# and Extract Frames
import os.path
import time
import base64
import json
import sys
from rq import Queue
from worker import conn
from utils import calling_frameAnalysis
from scene import CompareImage
# Function to extract frames
def FrameCapture(q,camara):
    # Path to video file
    #vidObj = cv2.VideoCapture(path)
    # Used as counter variable
    count = 1
    # checks whether frames were extracted
    success = 1
    path="/home/ubuntu/proyectos/microservicePlatanitos/pictures/"
    #path="/home/clara/FUENTES/microservicePlatanitos/pictures/"

    while(success):

        file = path+camara+"/"+"img"+str(count)+'.jpg';
        nameFile = "img"+str(count)+'.jpg';

        if count > 1:
            pastFile = path+camara+"/"+"img"+str(count-1)+'.jpg';

        #print("Analizando el file: ",file)

        while not os.path.exists(file):
            time.sleep(1)
            print("No encuentra file: ",file)

        if os.path.isfile(file):

            diff = float(1)

            if count > 1:
                diff = CompareImage(file,pastFile).compare_image()
                #print("diff: ",diff)

            if float(diff) >= 0.05:

                #print("Analizara imagen: ", file)
                with open(file, 'rb') as image:
                    free = bytearray(image.read())

                base64String = base64.b64encode(free);

                data = {"dataBytes": str(base64String)[2:][:-1],
                        "frame": nameFile,
                        "camara": camara}

                sale = q.enqueue(calling_frameAnalysis, data)
                #print(sale)

            if(count>3):
                print("Se removio: ",count)
                file2 = path+camara+"/"+"img"+str(count-2)+'.jpg';
                os.remove(file2)

            count += 1

        else:
            raise ValueError("%s isn't a file!" % file)


# Driver Code
if __name__ == '__main__':

    camera=sys.argv[1]
    print(camera)
    # Calling the function
    q = Queue(connection=conn)
    q.empty()
    FrameCapture(q,camera)
