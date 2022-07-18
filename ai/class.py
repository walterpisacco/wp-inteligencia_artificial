from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import io
import time
import numpy as np
#pip install opencv-python
import cv2
#pip install Pillow 
from PIL import Image
#pip3 install --extra-index-url https://google-coral.github.io/py-repo/ tflite_runtime
from tflite_runtime.interpreter  import Interpreter
#import tensorflow.keras as tk
#pip3 install paho-mqtt python-etcd
import paho.mqtt.client as mqtt
import base64
import pickle
import face_recognition
import sys, getopt
#import urllib.request

#pip install RPi.GPIO
#from gpio import gpio

from graf.common import clock, draw_str, draw_strApe, draw_rects, overlay_transparent

global client
global frameid
frameid = 0
client = mqtt.Client()
client.username_pw_set(username="walter",password="walter")
#client.connect('platform.drexgen.com', 1883, 60)
client.connect('ng.drexgen.com', 1883, 60)

# agregado para estreaming a
#Topico de Ejemplo = dsv/seg/hd/R00002PI04V0001/DPublica4
#Mensaje de Ejemplo= {"ID": "D00001IA01V0001", "Foto": "/9j/4AAQSkZJR....."}

#url = "https://platform.drexgen.com/dx-rrhh/img/faces/1/1.jpg?v=44"
#img = urllib.request.urlopen(url)
img = "static/graph/yo.jpg"
imagen_personal2 = face_recognition.load_image_file(img)  
personal_encodings2 = face_recognition.face_encodings(imagen_personal2)[0]    
encodings_conocidos = [personal_encodings2]
nombres_conocidos = ["Walter"]

def detect(img, cascade, rectsAnt):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30),flags=cv2.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        #rectsAnt[:,2:] += rectsAnt[:,:2]
        return rects,rectsAnt        
    else:
        rectsAnt = rects
    
    rects[:,2:] += rects[:,:2]
    return rects,rectsAnt

class classify(object):
  def __init__(self, camara='0',serie='',tipo='',label='',modelo='',opcion='',iot=''):
        self.LABELS=label #Cargo las etiquetas
        self.MODEL = modelo
        self.serie = serie
        self.tipo = tipo
        self.opcion = opcion
        self.iot = iot
        self.interpreter = None       
        self.input_cam = (camara) #indice de la Camara o rtsp
        self.video = cv2.VideoCapture(self.input_cam) #Cap de la camara
        self.ban = False #Bandera Para que cargue una sola Vez el Modelo YOLO
        self.labels = None #Donde Se carga el Detector
        self.ban1 = False
        self.conf = 0.9
        self.detector = cv2.CascadeClassifier('conv/haarcascade_frontalface_default.xml')
        self.anchoSalida = 400
        self.altoSalida = 320
        self.anchoAnalisis = 224
        self.altoAnalisis = 224        
        
        if(self.tipo == 'pickle'):
          self.data = pickle.loads(open(modelo, "rb").read())

        if(self.tipo == 'h5'):
          self.data = tk.models.load_model(modelo)

        args, video_src = getopt.getopt(sys.argv[1:], '', ['cascade=', 'nested-cascade='])
        args = dict(args)
        cascade_fn = args.get('--cascade', "conv/haarcascade_frontalface_alt.xml")
        nested_fn  = args.get('--nested-cascade', "conv/haarcascade_eye.xml") 
        self.cascade = cv2.CascadeClassifier(cv2.samples.findFile(cascade_fn))
        self.nested = cv2.CascadeClassifier(cv2.samples.findFile(nested_fn))          

        #self.gpio = gpio(21, True)

  def load_labels(self,path):
    
    with open(path, 'r') as f:
      return {i: line.strip() for i, line in enumerate(f.readlines())}

  def set_input_tensor(self,interpreter, image):
    tensor_index = interpreter.get_input_details()[0]['index']
    input_tensor = interpreter.tensor(tensor_index)()[0]
    input_tensor[:, :] = image
    
  def classify_image(self,interpreter, image, top_k=1):
    self.set_input_tensor(interpreter, image)
    interpreter.invoke()
    output_details = interpreter.get_output_details()[0]
    output = np.squeeze(interpreter.get_tensor(output_details['index']))
    if output_details['dtype'] == np.uint8:
      scale, zero_point = output_details['quantization']
      output = scale * (output - zero_point)
    ordered = np.argpartition(-output, top_k)
    return [(i, output[i]) for i in ordered[:top_k]]

  def __del__(self):
      self.video.release()
      print("borrado")

  def get_frame(self):
      #cv2.waitKey(100)
      #opcion del select filterInput (opciones deltro del txt seleccionado)
      opcion  = self.opcion
      iot       = self.iot
      success, frame = self.video.read()
      frameOriginal = cv2.resize(frame,(self.anchoSalida,self.altoSalida))
      size = (self.anchoAnalisis, self.altoAnalisis)
      frame = cv2.resize(frame, size)
      if success:
        if self.tipo == 'tflite':
          marco = self.main_tflite(frameOriginal,frame,opcion,iot)
          analitica = 'od'

        if self.tipo == 'pickle':
          marco = self.main_fr(frameOriginal,frame,opcion,iot)
          analitica = 'hd'

        if self.tipo == 'h5':
          marco = self.main_h5(frameOriginal,frame,opcion,iot)
          analitica = 'od'

        topicFoto = 'dsv/seg/'+analitica+'/'+self.serie+'/DPublica4'
        topicResp = 'dsv/seg/'+analitica+'/'+self.serie+'/DPublica2'

        ret,jpeg = cv2.imencode('.jpg', marco)
        salida =  jpeg.tobytes()
        # bajo los frames a 1 de 5 para mandarlos por mqtt
        global frameid
        if frameid%50==0:
          fotobase64 = base64.b64encode(salida).decode('utf-8')
          msgFoto = '{"ID": "'+self.serie+'", "Foto": "'+fotobase64+'"}'
          cv2.waitKey(10)
          respuesta = client.publish(topicFoto,payload=msgFoto,qos=0)
          print(topicFoto)

        frameid += 1
        return salida
      else:
          print ("error")

  def stream(self, camera):
      return camera
  def main_tflite(self,frameOriginal,frame,opcion,iot):
    if self.ban == False:
      with open(self.LABELS, 'r') as f:
        self.labels = {i: line.strip() for i, line in enumerate(f.readlines())}
      self.interpreter = Interpreter(self.MODEL)
      self.interpreter.allocate_tensors()
      _, height, width, _ = self.interpreter.get_input_details()[0]['shape']
      self.ban = True
    
    overlay = cv2.imread('static/graph/ventana.png', cv2.IMREAD_UNCHANGED)
    overlay = cv2.resize(overlay, (180,60))
    overlay_transparent(frameOriginal, overlay, 5, 5)

    image_array = np.asarray(frame)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    start_time = time.time()
    results = self.classify_image(self.interpreter, normalized_image_array)
    
    elapsed_ms = (time.time() - start_time) * 1000
    text = self.labels[results[0][0]]
    text = text.split (" ")

    if(int(text[0]) == int(opcion) and int(iot) == 1):
      if self.ban1 == False:
        print('SUENA ALARMA!!')
        print ("true")
        #self.gpio.upin()
        self.ban1 = True
      elif (int(text[0]) == int(opcion) and int(iot) == 0):
        self.ban1 = False

    texto = text[1]

    if(int(text[0]) == 0):
      color = (0, 160, 255)
    else:
      color = (0, 0, 255)

    draw_strApe(frameOriginal, (20, 40), texto,color) 
    return frameOriginal

  def main_fr(self,frameOriginal,frame,opcion,iot):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    marco = self.face_reco(frameOriginal,frame, gray, rgb)
    return marco

  def main_h5(self,frameOriginal, frame,opcion,iot):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image_array=np.asarray(frame)
    normalize_image = (image_array.astype(np.float32) / 127.0) - 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalize_image
    prediction = self.data.predict(data)

    overlay = cv2.imread('static/graph/ventana.png', cv2.IMREAD_UNCHANGED)
    overlay = cv2.resize(overlay, (180,60))
    overlay_transparent(frameOriginal, overlay, 5, 5)
    
    draw_strApe(frameOriginal, (15, 40), 'texto',(0, 0, 255)) 

    #label, color = texto(prediction)
    return frameOriginal

  def face_reco(self,frameOriginal,frame,gray,rgb):
    rectsAnt = []
    #rects = self.detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
    rects,rectsAnt = detect(gray, self.cascade,rectsAnt)
    vis = frame.copy()

    loc_rostros = face_recognition.face_locations(vis)
    encodings = face_recognition.face_encodings(vis, loc_rostros)    

  #  t = clock()
  #  dt = clock() - t
  #  valor = ('%sK' % (dt/1000))[:4]
    if len(rects) > 0:
        rects[:,2:] += rects[:,:2]
        for x1, y1, x2, y2 in rects:
            centrox = int((x1 + x2 ) / 2)
            centroy = int((y1 + y2 ) / 2)
            draw_rects(frameOriginal, rects, (0, 255, 0))
            overlay = cv2.imread('static/graph/ventana.png', cv2.IMREAD_UNCHANGED)
            overlay = cv2.resize(overlay, (180,60))
            overlay_transparent(frameOriginal, overlay, centrox + 30, centroy)
            #draw_str(frame, (10,10), valor)
        #encodings = face_recognition.face_encodings(rgb, rects)
        #encodings = []
        names = []
        for encoding in encodings:
            coincidencias = face_recognition.compare_faces(encodings_conocidos, encoding)
            #coincidencias = face_recognition.compare_faces(self.data['encodings'],encoding)
            if True in coincidencias:
                name = nombres_conocidos[coincidencias.index(True)]
              #  matchedIdxs = [i for (i, b) in enumerate(coincidencias) if b]
              #  counts = {}
              #  for i in matchedIdxs:
              #      name = self.data['names'][i]
              #      counts[name] = counts.get(name, 0) + 1
              #  name = max(counts, key=counts.get)
              #  name = nombres_conocidos[0]

                #Topico de Ejemplo = dsv/seg/hd/D00001IA01V0001/DPublica4
                #Mensaje de Ejemplo= {"modelo": "face_reco", "serial": "R00001PI04V0001", "predictions": [{"Detecciones": ["Cristian Luna"]}]}
                #msg = '{"modelo": "face_reco", "serial": "'+serie+'", "predictions": [{"Detecciones": ["'+name+'"]}]}'
                #client.publish(topicResp,payload=msg,qos=0)
                for x1, y1, x2, y2 in rects:
                    centrox = int((x1 + x2 ) / 2)
                    centroy = int((y1 + y2 ) / 2)
                    draw_strApe(frameOriginal, (centrox + 50, centroy + 20), name,(0, 160, 255))
    return frameOriginal 
  