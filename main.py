from flask import Flask, render_template, redirect, request, flash, jsonify, Response, url_for
import flask

import json
import re
import os
import zipfile

from werkzeug.utils import secure_filename
#from flask_jsglue import JSGlue
from ai.ITFLapi import ident
from ai.ITFL import inicializarITFL
from ai.FRs import inicializarFRs
from ai.Face import inicializarFace
from ai.Hands import inicializarHands
from ai.H5 import inicializarH5
from ai.alpr import inicializarALPR

#pip install opencv-python
import cv2
#pip3 install flask-mysql
from flaskext.mysql import MySQL

import base64
from PIL import Image
import io
import random

from imutils import paths
import face_recognition
import pickle
import shutil

#
mysql = MySQL()

app = Flask(__name__ , template_folder= "modulos")
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

from config import config
configuracion = config()

# MySQL configurations
app.config['UPLOAD_FOLDER'] = configuracion.pathModelos
app.config['MYSQL_DATABASE_USER'] = configuracion.usuario
app.config['MYSQL_DATABASE_PASSWORD'] = configuracion.password
app.config['MYSQL_DATABASE_DB'] = configuracion.base
app.config['MYSQL_DATABASE_HOST'] = configuracion.servidor

app.config['URL_API'] = configuracion.urlApi

mysql.init_app(app)

idCamara = 0
label = ''
modelo = ''
opcion = ''
iot = 'false'
global idCliente
idCliente = 6

from json import load
from urllib.request import urlopen
#my_ip = load(urlopen('http://jsonip.com'))['ip']
#my_ip = flask.request.remote_addr

#busco el cliente de una sesion de usuario de la plataforma conectada desde esta ip
conn = mysql.connect()
cursor = conn.cursor()

def validasession():
	'''my_ip = flask.request.remote_addr
	my_ip='152.171.224.204'	

	query = "select p.idCliente from dx_personal.logs l join dx_personal.seg_usuarios su on l.idUsuario = su.idUsuario join dx_personal.personas p on su.idPersona = p.idPersona where conectado = 1 and ip = '"+ str(my_ip)+"'"
	cursor.execute(query)
	conn.commit()
	results = cursor.fetchall()
	if len(results) > 0:
		for row in results:
			global idCliente
			idCliente = row[0]'''

	return 

@app.route('/error', methods = ['GET', 'POST'])
def error():
    return render_template('error.html')

@app.route('/', methods = ['GET', 'POST'])
def index():
	validasession()
	return render_template('index.html')

@app.route('/equipos', methods = ['GET', 'POST'])
def equipos():
	#validasession()
	return render_template('equipos/index.html')

@app.route('/configuracion', methods = ['GET', 'POST'])
def configuracion():
	#validasession()
	return render_template('configuracion/index.html')

@app.route('/entrenamiento', methods = ['GET', 'POST'])
def entrenamiento():
	#validasession()
	return render_template('entrenamiento/index.html')

@app.route('/modelos', methods = ['GET', 'POST'])
def modelos():
	#validasession()
	return render_template('modelos/index.html')

@app.route("/Combos_get", methods=["GET","POST"])
def Combos_get():
	conn = mysql.connect()
	cursor = conn.cursor()
	_oUsu = '1'
	_idCliente = idCliente
	_tipo = request.form.get("tipo")
	_param = request.form.get("param")

	cursor.callproc('dsv_dev.Combo_get',(_idCliente, _tipo, _param ))
	data = cursor.fetchall()
	return json.dumps(data)

@app.route("/EquiposList_get", methods=["GET","POST"])
def EquiposList_get():
	conn = mysql.connect()
	cursor = conn.cursor()
	_oUsu = '1'
	_idCliente = idCliente

	_where = ' where e.idCliente = '+ str(_idCliente)+' and e.estado <>3 '
	_start = '1'
	_limit = '1000'
	_sidx = '1'
	_sord = 'asc'	

	cursor.callproc('dsv_dev._Rasp_Equipos_Listar',(_oUsu,_where,_start,_limit,_sidx,_sord))
	data = cursor.fetchall()
	return json.dumps(data)

@app.route("/Equipo_Guardar", methods=["GET","POST"])
def Equipo_Guardar():
	conn = mysql.connect()
	cursor = conn.cursor()
	_oUsu = '1'
	_idCliente = idCliente
	_idEquipo = request.form.get("idEquipo")
	_tipo 	= request.form.get("tipo")
	_estado = request.form.get("estado")
	_nombre = request.form.get("nombre")
	_marca 	= request.form.get("marca")
	_serie 	= request.form.get("serie")
	_dir 	= ''
	_lat 	= ''
	_lon 	= ''

	cursor.callproc('dsv_dev._Rasp_Equipo_Guardar',(_oUsu, _idCliente, _idEquipo, _tipo, _estado, _nombre, _marca, _serie, _dir, _lat, _lon))
	data = cursor.fetchall()
	conn.commit()
	return json.dumps(data)

@app.route("/Equipo_Eliminar", methods=["GET","POST"])
def Equipo_Eliminar():
	conn = mysql.connect()
	cursor = conn.cursor()
	_oUsu = '1'
	_idCliente = idCliente
	_idEquipo = request.form.get("idEquipo")

	cursor.callproc('dsv_dev._Rasp_Equipo_Eliminar',(_oUsu, _idEquipo))
	data = cursor.fetchall()
	conn.commit()
	return json.dumps(data)	

@app.route("/DispositivosList_get", methods=["GET","POST"])
def DispositivosList_get():
	conn = mysql.connect()
	cursor = conn.cursor()
	_oUsu = '1'
	_idCliente = idCliente

	_where = ' where dsv_estado <> 3 and dsv_user_id = '+ str(_idCliente)
	_start = '1'
	_limit = '1000'
	_sidx = '1'
	_sord = 'asc'	

	cursor.callproc('dsv_dev._Rasp_DSV_Listar',(_oUsu,_where,_start,_limit,_sidx,_sord))
	data = cursor.fetchall()
	return json.dumps(data)

@app.route("/Dispositivo_Eliminar", methods=["GET","POST"])
def Dispositivo_Eliminar():
	conn = mysql.connect()
	cursor = conn.cursor()
	_oUsu = '1'
	_idCliente = idCliente
	_idDispositivo = request.form.get("idDispositivo")

	cursor.callproc('dsv_dev._Rasp_Dispositivo_Eliminar',(_oUsu,_idDispositivo))
	data = cursor.fetchall()
	conn.commit()
	return json.dumps(data)	

@app.route("/DispositivoModelo_get", methods=["GET","POST"])
def DispositivoModelo_get():
	conn = mysql.connect()
	cursor = conn.cursor()
	_oUsu = '1'
	_idCliente = idCliente

	cursor.callproc('dsv_dev._Rasp_Modelos_Get',(_oUsu,_idCliente))
	data = cursor.fetchall()
	return json.dumps(data)	

@app.route("/Dispositivo_Guardar", methods=["GET","POST"])
def Dispositivo_Guardar():
	conn = mysql.connect()
	cursor = conn.cursor()
	_oUsu = '1'
	_idCliente = idCliente

	_idDispositivo 	= request.form.get("idDispositivo")
	_equipo 		= request.form.get("equipo")
	_tipo 			= request.form.get("tipo")
	_marca 			= request.form.get("marca")
	_camara		 	= request.form.get("webcamInput")
	_rtsp 			= request.form.get("ruta")
	_serie 			= request.form.get("serie")
	_nombre 		= request.form.get("nombre")
	_modelo 		= request.form.get("modelo")
	_modeloDesc 	= request.form.get("modeloDesc")
	_modeloTxt 		= request.form.get("modeloTxt")
	_analitica 		= request.form.get("analitica")
	_estado 		= 1
	_comu1 			= request.form.get("comu1")
	_comu2 			= request.form.get("comu2")
	_comu3 			= request.form.get("comu3")
	_comu4 			= request.form.get("comu4")
	_comu5 			= request.form.get("comu5")
	_comu6 			= request.form.get("comu6")
	_view 			= request.form.get("view")
	_dron 			= request.form.get("dron")	
	_usuario = ''
	_password = ''

	cursor.callproc('dsv_dev._Rasp_DSV_Guardar',(_oUsu, _idCliente,_idDispositivo,_equipo,_tipo,_marca,_camara,_rtsp,_serie,
	_nombre,_modelo,_analitica,_estado,_comu1,_comu2,_comu3,_comu4,_comu5,_comu6,_view,_dron,_usuario,_password))
	
	data = cursor.fetchall()
	conn.commit()

	datos={
		    "configuracion":[{
		        "cap":_camara,
		        "conf":0.6,
				"id" : 		_idDispositivo, 	
				"equipo": 	_equipo, 			
				"tipo" : 	_tipo, 			
				"marca": 	_marca, 			
				"camara":  	_camara,		 	
				"rtsp" : 	_rtsp, 			
				"serie": 	_serie, 			
				"nombre":  	_nombre,
				"modeloPath":app.config['UPLOAD_FOLDER'], 		
				"modeloID":  _modelo,
				"modeloDesc":  _modeloDesc,
				"modeloTxt":  _modeloTxt, 		
				"analitica":_analitica, 		
				"estado":  	_estado, 		
				"mail": 	_comu1, 			
				"telegram": 	_comu2, 			
				"whatsApp": 	_comu3, 			
				"http": 	_comu4, 			
				"clienteApi": 	_comu5, 			
				"mqtt": 	_comu6, 			
				"pin" : 	_view, 			
				"dron" : 	_dron 				
		        }
		    ]
		}

	with open('data/autorun.json', 'w') as file:
		json.dump(datos, file)

	return json.dumps(data)	

@app.route("/DispositivoBLE_Guardar", methods=["GET","POST"])
def DispositivoBLE_Guardar():
	conn = mysql.connect()
	cursor = conn.cursor()
	_oUsu = '1'
	_idCliente = idCliente

	_idBLE 			= request.form.get("idBLE")
	_equipo			= request.form.get("equipoBLE")	
	_tipo 			= request.form.get("tipoBLE")
	_marca 			= request.form.get("marcaBLE")
	_serie 			= request.form.get("serieBLE")
	_nombre 		= request.form.get("nombreBLE")
	_estado 		= 1
	_usuario = ''
	_password = ''


	#print(_oUsu)
	#print(_idCliente)
	#print(_idBLE)
	#print(_equipo)
	#print(_tipo)
	#print(_marca)
	#print(_serie)
	#print(_nombre)
	#print(_estado)

	cursor.callproc('dsv_dev._Rasp_DSV_Guardar',(_oUsu, _idCliente,_idBLE,_equipo,_tipo,_marca,'ble','',_serie,
	_nombre,0,0,_estado,'','','','','','','','',_usuario,_password))
	
	data = cursor.fetchall()
	conn.commit()
	return json.dumps(data)

@app.route("/Modelos_get", methods=["GET","POST"])
def Modelos_get():
	conn = mysql.connect()
	cursor = conn.cursor()
	_oUsu = '1'
	_idCliente = idCliente

	cursor.callproc('dsv_dev._Rasp_Modelos_Get',(_oUsu,_idCliente))
	data = cursor.fetchall()
	return json.dumps(data)

@app.route("/ModelosList_get", methods=["GET","POST"])
def ModelosList_get():
	conn = mysql.connect()
	cursor = conn.cursor()
	_oUsu = '1'
	_idCliente = idCliente

	_where = ' where m.idCliente = '+ str(idCliente)
	_start = '1'
	_limit = '1000'
	_sidx = '1'
	_sord = 'asc'	

	cursor.callproc('dsv_dev._Rasp_Modelos_Listar',(_oUsu,_where,_start,_limit,_sidx,_sord))
	data = cursor.fetchall()
	return json.dumps(data)

@app.route("/Modelo_Guardar", methods=["GET","POST"])
def Modelo_Guardar():
	conn = mysql.connect()
	cursor = conn.cursor()
	_oUsu = '1'
	_idCliente = idCliente
	_tipo = request.form.get("tipo")
	_modelo = request.form.get("modelo")
	_descripcion = request.form.get("descripcion")

	if request.method == 'POST':
		file = request.files['file']
		if file: #and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			x = filename.split(".")
			extension = x[len(x)-1]
			nuevoNombre = _modelo+'.'+extension
			ruta = os.path.join(app.config['UPLOAD_FOLDER'])
			rutaCompleta = os.path.join(app.config['UPLOAD_FOLDER'], nuevoNombre)
			file.save(rutaCompleta)
			cursor.callproc('dsv_dev._Rasp_Modelos_Guardar',(_oUsu,_idCliente,_tipo,_modelo,_descripcion))
			conn.commit()
			records = cursor.fetchone()
			_idModelo = records[0]
			if _idModelo > 0:
				if extension == 'zip':
					zf = zipfile.ZipFile(rutaCompleta, "r")
					for member in zf.infolist():
						words = member.filename.split('/')
						path = ruta
						for word in words[:-1]:
							drive, word = os.path.splitdrive(word)
							head, word = os.path.split(word)
							if word in (os.curdir, os.pardir, ''): continue
							path = os.path.join(path, word)
						x = member.filename.split(".")
						extension = x[len(x)-1]
						member.filename = _modelo+'.'+extension
						zf.extract(member, path)
						cursor.callproc('dsv_dev._Rasp_ModelosArchivos_Guardar',(_oUsu,_idModelo,_modelo,member.filename))
						conn.commit()
						records = cursor.fetchone()
				else:
						cursor.callproc('dsv_dev._Rasp_ModelosArchivos_Guardar',(_oUsu,_idModelo,_modelo,nuevoNombre))
						conn.commit()
			else:
				return jsonify({'Text': 'ERROR AL INTENTAR SUBIR EL MODELO, INTENTE NUEVAMENTE!!'})


		return jsonify({'Text': 'Modelo subido con exito!!'})
	return 'NOT_POST'

@app.route("/Modelo_Eliminar", methods=["GET","POST"])
def Modelo_Eliminar():
	conn = mysql.connect()
	cursor = conn.cursor()
	_oUsu = '1'
	_idCliente = idCliente
	_idModelo = request.form.get("idModelo")

	cursor.callproc('dsv_dev._Rasp_Modelo_Eliminar',(_oUsu,_idModelo))
	data = cursor.fetchall()
	conn.commit()
	return json.dumps(data)

@app.route("/EquiposModelos_guardar", methods=["GET","POST"])
def EquiposModelos_guardar():
	conn = mysql.connect()
	cursor = conn.cursor()
	_oUsu = '1'
	_idCliente = idCliente
	_idDSV = request.form.get("idDSV")
	_webcam = request.form.get("webcam")
	_rtsp = request.form.get("rtsp")
	_idModelo = request.form.get("idModelo")	

	cursor.callproc('dsv_dev._Rasp_EquiposModelos_Guardar',(_oUsu,_idDSV,_webcam,_rtsp,_idModelo))
	data = cursor.fetchall()
	return json.dumps(data)

@app.route('/labels', methods=["GET","POST"])
def labels():
	_txtmodelo = request.form.get("txtmodelo")
	nnline = []
	with open(app.config['UPLOAD_FOLDER']+_txtmodelo) as file:
		file.seek(0)
		text = file.readlines()
		for lines in text:
			newline = []
			value = re.search(r'([0-9]+)\s([A-Za-z0-9\s\.]+)', lines, re.M|re.I)
			if value:
				if value.group(1):
					val=value.group(1)
					newline.append(val)
				if value.group(2):
					val=value.group(2)
					newline.append(val)
				if newline:
					nnline.append(newline)
	if nnline:
		return jsonify(nnline)
	return jsonify({'error': 'Algo paso'})

@app.route('/recibirGuardarImagen', methods=['POST'])
def recibir():
	target_dir = 'uploads/'
	datum = datetime.datetime.now()
	datum = datum.strftime("%Y%m%d_%H%M%S")
	target_file = target_dir+datum;
	uploadOk = 1
	validas = ['jpg','jpeg','png','gif']
	if flask.request.method == "POST":
		file = flask.request.files.get("imageFile")
		if file:
			filename = secure_filename(file.filename)
			target_file = target_file+'_'+filename
			uploadOk = 1
			print('El archivo es una imagen.')
		else:
			uploadOk = 0
			print('El archivo no es una imagen.')

	if path.exists(target_file):
		return jsonify({'error': 'Uuuh! Este archivo ya existe. ¿Qué intentas?'})
		uploadOk = 0

	blob = file.read()
	size = len(blob)
	if size > 500000:
		return jsonify({'error': 'Uuuh! Este archivo pesa mucho. ¡Vuelve a intentarlo!'})
		uploadOk = 0

	ext = filename.split(".")
	ext = ext[len(ext)-1]
	if ext not in validas:
		return jsonify({'error': 'Uuuh! Este archivo no es válido. ¡Vueleve a intentarlo!'})
		uploadOk = 0

	if uploadOk==0:
		return jsonify({'error': 'Lamentablemente tu archivo no puede ser subido.'})
	else:
		image = Image.open(io.BytesIO(blob))
		image_array = np.asarray(image)
		cv2.imwrite(target_file,image_array)
		if path.exists(target_file):
			# cambiar jarcodeada por los parametros extraidas de la base
			procesar=ident('derxgen_esp32',app.config['UPLOAD_FOLDER'] +'modelo.txt',app.config['UPLOAD_FOLDER'] +'modelo.tflite','1','0')
			procesar.main_tflite(image)
			return jsonify({'success': 'Imagen guardada con exito, en ruta: .'+target_file})
		else:
			return jsonify({'error': 'Hubo algún problema subiendo tu imagen.'})

	return jsonify({'error': 'Algo no ando bien.'})


@app.route('/process', methods=['POST'])
def process():
	#indico que debe grabar en la variable global porque dentro de las funciones, las globales  son solo lectura
    global idCamara
    global serie
    global tipo
    global label
    global modelo
    global opcion
    global iot
    global webcamId

    if request.form['webcam'].isnumeric():
        idCamara = int(request.form['webcam'])
    else:
        idCamara = request.form['webcam']

    serie 		= request.form['serie']
    webcamId	= request.form['webcamId']
    tipo 		= request.form['tipo']
    label 		= app.config['UPLOAD_FOLDER'] + request.form['label']
    modelo 		= app.config['UPLOAD_FOLDER'] + request.form['modelo']
    opcion 		= request.form['opcion']
    iot 		= request.form['iot']

    return jsonify({'success': idCamara})

def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
	global VS
	if tipo == 'pickle':
		camera = read()
		VS = inicializarFRs(idCamara,webcamId,serie,tipo,label,modelo,opcion,iot,app.config['URL_API'])

	if tipo == 'tflite':
		pass
		VS = inicializarITFL(idCamara,webcamId,serie,tipo,label,modelo,opcion,iot,app.config['URL_API'])

	if tipo == 'entrenar':
		pass
		VS = inicializarFace(idCamara,webcamId,serie,tipo,label,modelo,opcion,iot,app.config['URL_API'])

	if tipo == 'hands':
		pass
		VS = inicializarHands(idCamara,webcamId,serie,tipo,label,modelo,opcion,iot,app.config['URL_API'])

	if tipo == 'h5':
		pass
		VS = inicializarH5(idCamara,webcamId,serie,tipo,label,modelo,opcion,iot,app.config['URL_API'])

	if tipo == 'alpr':
		pass
		VS = inicializarALPR(idCamara,webcamId,serie,tipo,label,modelo,opcion,iot,app.config['URL_API'])

	vargen = gen(VS) 
	salida = Response(vargen,mimetype='multipart/x-mixed-replace; boundary=frame')
	return salida

@app.route('/processObtenerVideo', methods=['POST'])
def processObtenerVideo():
	global camara
	global serie
	global tiposalida
	global nombreArchivo
	
	if request.form['webcam'].isnumeric():
		camara = int(request.form['webcam'])
	else:
		camara = request.form['webcam']

	serie= request.form['serie']
	tiposalida= request.form['tiposalida']
	nombreArchivo= request.form['nombreArchivo']
	
	return jsonify({'success': serie})

@app.route('/video_feed_obtener')
def video_feed_obtener():
	from datetime import datetime
	now = datetime.now()
	carpeta = now.strftime("%H%M%S")
	os.mkdir(carpeta)	
	pass
	varini = capturar(camara,serie,carpeta,tiposalida,nombreArchivo)
	vargen = gen_obtener(varini) 	
	salida = Response(vargen,mimetype='multipart/x-mixed-replace; boundary=frame')

	return salida

def gen_obtener(camera):
    while True:
        frame = camera.get_frame_captura()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed_detener')
def video_feed_detener():
	if 'VS' in globals():
		global VS
		inicializarITFL.detener_frame(VS)
	
	return "detenido"

def read():
    f = open('data/autorun.json')
    data = json.load(f)
    for i in data['configuracion']:
        camera = i['cap']
    f.close()
    return camera

@app.route("/Imagen_Guardar", methods=["GET","POST"])
def Imagen_Guardar():
	_name = request.form.get("name").lower()
	_imgbase64 = request.form.get("imgbase64")

	_imgbase64 = _imgbase64[22:]
	image = base64.b64decode(str(_imgbase64))     

	img = Image.open(io.BytesIO(image))

	nombre = 'static/dataset/'+_name+'/'+_name+'__'+str(random.randrange(1, 10000, 1))+'.png'

	try:
		os.mkdir('static/dataset/'+_name)
		img.save(nombre, 'png')
	except OSError as e:
		img.save(nombre, 'png')

	return 'ok'

@app.route("/Imagen_Entrenar", methods=["GET","POST"])
def Imagen_Entrenar():
	try:
		video_feed_detener()

		path = app.config['UPLOAD_FOLDER']+"faces.pickle"
		os.remove(path)
		print("% s removed successfully" % path)
	except OSError as error:
		print("Archivo no encontrado para borrar")

	print("[DREXGEN] contando rostros...")
	imagePaths = list(paths.list_images('static/dataset'))
	knownEncodings = []
	knownNames = []

	valid_images = [".jpg",".png"]

	for (i, imagePath) in enumerate(imagePaths):
		ext = os.path.splitext(imagePath)[1]
		if ext.lower() in valid_images:
			print("[DREXGEN] procesando imagenes {}/{}".format(i + 1,len(imagePaths)))
			name = imagePath.split(os.path.sep)[-2]
			image = cv2.imread(imagePath)
			rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

			boxes = face_recognition.face_locations(rgb,model="cnn")
			encodings = face_recognition.face_encodings(rgb, boxes)
			for encoding in encodings:
				knownEncodings.append(encoding)
				knownNames.append(name)
				print("[DREXGEN] codificando... "+str(name))

	print("[DREXGEN] fin de la codificacion...")
	data = {"encodings": knownEncodings, "names": knownNames}
	f = open(app.config['UPLOAD_FOLDER'] +'faces.pickle', "wb")
	f.write(pickle.dumps(data))
	f.close()

	return jsonify({'success': 'true'})

@app.route("/Imagen_Buscar", methods=["GET","POST"])
def Imagen_Buscar():

	imagePaths = list(paths.list_images('static/dataset'))
	valid_images = [".jpg",".png"]

	respuesta = '['
	for (i, imagePath) in enumerate(imagePaths):
		respuesta += '{"imagen":"'+imagePath+'"},'
		print(imagePath)

	respuesta = respuesta[:-1] + ']'
	print(respuesta)
	return jsonify(respuesta)

@app.route("/Imagen_Limpiar", methods=["GET","POST"])
def Imagen_Limpiar():
	carpetas = os.listdir('static/dataset')
	try:
		for carpeta in carpetas:
			shutil.rmtree('static/dataset/'+carpeta)
	except OSError as e:
		print("Error: %s: %s" % (carpetas, e.strerror))

	return jsonify({'success': 'true'})

if __name__ == '__main__':
    debug = True #toma los cambios sin reiniciar
    #app.run(host='127.0.0.1', debug=True)
    #app.run(host='0.0.0.0', port= 4000, debug=True, ssl_context='adhoc')
    app.run(host='0.0.0.0', port= 4100, debug=True)
     
