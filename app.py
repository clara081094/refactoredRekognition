from flask import Flask
from microservices.frameAnalysis import FrameAnalysis
from microservices.reportAnalysis import ReportAnalysis
from flask import send_file
from flask import request
from flask import abort
import json

app = Flask(__name__)

@app.route("/")
def hello():
   return "HELLO"

@app.route('/retornarFace/<place>/<face>')
def return_face(place,face):
	try:
		return send_file('/home/ubuntu/proyectos/microservicePlatanitos/pictures/'+(place)+'/registered/'+(face), attachment_filename=(face))
	except Exception as e:
		return str(e)

@app.route('/retornarImagen/<place>/<imagen>')
def return_image(place,imagen):
	try:
		return send_file('/home/ubuntu/proyectos/microservicePlatanitos/pictures/'+(place)+"/"+(imagen), attachment_filename=(imagen))
	except Exception as e:
		return str(e)

@app.route('/procesarFrame', methods=['POST'])
def process_frame():
   print(request)
   if not request.json :
      abort(400)
   else :
      FrameAnalysis().process(request.json)
      return json.dumps({'process':'success'})

@app.route('/reporte', methods=['POST'])
def get_reports():
   if not request.json:
      abort(400)
   else :
      return json.dumps(ReportAnalysis().day_Report(request.json))

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)
