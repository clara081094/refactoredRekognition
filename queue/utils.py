import requests
import json

def calling_frameAnalysis(dato):

    #url = "http://ec2-3-84-39-95.compute-1.amazonaws.com:5000/procesarFrame"
    url = "http://localhost:5000/procesarFrame"
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    r = requests.post(url, data=json.dumps(dato), headers=headers)
