import boto3
import json
#from botocore.exceptions import ClientError


class Rekognition(object):

    def __init__(self):
        self.client = boto3.client('rekognition',
	region_name="us-east-1",
	aws_access_key_id="AKIAIMM524QL43QPT43A",
        aws_secret_access_key="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")

    def detect_faces(self,bytess):

        response = self.client.detect_faces(
            Image={'Bytes': bytess }, Attributes=['ALL'])

        return response

    def face_recog(self,bytess,collectionId):
    
        try:    
            response = self.client.search_faces_by_image(
                CollectionId=collectionId,
                Image={
                    'Bytes': bytess
                },
                FaceMatchThreshold=75
            )
            return response
        except:
            print("Error over face")
            return "BAD"
        
    

    def index_faces(self,bytess,collectionId,idImage):

        try:
            response = self.client.index_faces(
            Image={'Bytes': bytess}, CollectionId=collectionId, ExternalImageId=idImage)
            return response
        except:
            print("Error over face")
            return "BAD"


