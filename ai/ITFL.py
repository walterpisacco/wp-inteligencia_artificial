from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import io
import time
import numpy as np
#pip install opencv-python jaja
import cv2
#pip install Pillow 
from PIL import Image
#pip3 install --extra-index-url https://google-coral.github.io/py-repo/ tflite_runtime
from tflite_runtime.interpreter  import Interpreter
#import tensorflow.keras as tk
#pip3 install paho-mqtt python-etcd
import base64
import sys, getopt
import threading
#import RPi.GPIO as GPIO

#pip install RPi.GPIO
#from gpio import gpio

from common import clock, draw_str, draw_strApe, draw_rects, overlay_transparent
#from send.send import eventosImagen
import requests
import json

global client
global frameid
frameid = 0
global URLMQTT
URLMQTT = ''

class inicializarITFL(object):
  def __init__(self, camara='0',webcamId='0',serie='',tipo='',label='',modelo='',opcion='',iot='',dsvApi=''):
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
        self.anchoSalida = 400
        self.altoSalida = 320
        self.anchoAnalisis = 224
        self.altoAnalisis = 224
        self.dsvApi = dsvApi         
        self.topic = f'dsv/seg/od/{self.serie}/DPublica4'
        self.topicDronON = f'dsv/seg/od/{self.serie}/DronON'
        self.topicDronOFF = f'dsv/seg/od/{self.serie}/DronOFF'
   
        #self.gpio = gpio(21, True)

        #** Obtengo desde la base los mensajes de salida que tiene configurada la camara
        # y lo guardo en un array para usarlo en send_api
        payload={}
        headers = {}
        urlMensaje = dsvApi+"mensajestipo/"+serie
        #self.arrMensajes = requests.request("GET", urlMensaje, headers=headers, data=payload).json()
        #print(type(self.arrMensajes))
        #********************************************************************************

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

  def detener_frame(self):
      self.video.release()
      print("borrado")

  def get_frame(self):
      #opcion del select filterInput (opciones deltro del txt seleccionado)
      opcion  = self.opcion
      iot     = self.iot
      success, self.frame = self.video.read()

      frameOriginal = cv2.resize(self.frame,(self.anchoSalida,self.altoSalida))

      size = (self.anchoAnalisis, self.altoAnalisis)
      self.frame = cv2.resize(self.frame, size)
      if success:
        self.tipo == 'tflite'
        marco = self.main_tflite(frameOriginal,self.frame,opcion,iot)
        analitica = 'od'

        ret,jpeg = cv2.imencode('.jpg', marco)
        salida =  jpeg.tobytes()

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
        self.send_api()
        self.encender(self.ban1)
        timer = threading.Timer(5.0, self.encender)
        timer.start()
        self.ban1 = True
        #frametimer = threading.Timer(0.5,self.send_api, arg=frame)
      elif (int(text[0]) == int(opcion) and int(iot) == 0):
        self.ban1 = False

    texto = text[1]

    if(int(text[0]) == 0):
      color = (0, 160, 255)
    else:
      color = (0, 0, 255)

    draw_strApe(frameOriginal, (20, 45), texto,color) 

    return frameOriginal

  def encender(self, state=True):
      #GPIO.setmode(GPIO.BCM) 
      #GPIO.setup(21, GPIO.OUT)
      #GPIO.output(21, GPIO.HIGH)
      if state== False:
          print("ACTIVA PIN")        
          #GPIO.output(21, GPIO.LOW)# Turn off
      else:
          print("DESACTIVA PIN")
          #GPIO.output(21, GPIO.HIGH)# Turn on
          self.ban1=False

  def send_api(self):
    tipo = ''
    IMAGE = self.frame
    ret,jpeg = cv2.imencode('.jpg', IMAGE)
    salida =  jpeg.tobytes()
    fotobase64 = base64.b64encode(salida).decode('utf-8')

    #recorro los mensajes que tiene configurada la camara
    #1 Email
    #2 telegram
    #3 WhatsApp
    #4 Http
    #5 Cliente API
    #6 MQTT
    #7 GPIO   
    '''
    for mensaje in self.arrMensajes:
      if mensaje["id"] == 1:
        print('Mail:',mensaje["valor"])

      if mensaje["id"] == 2:
        print('Telegram:',mensaje["valor"])

      if mensaje["id"] == 3:
        print('WhatsApp:',mensaje["valor"])        

      if mensaje["id"] == 4:
        print('Http:',mensaje["valor"])

      if mensaje["id"] == 5:
        print('Cliente API:',mensaje["valor"])

      if mensaje["id"] == 6:
        global URLMQTT
        URLMQTT = mensaje["valor"]
        print('MQTT:',mensaje["valor"])
        tipo = mensaje["tipo"]
        valor = mensaje["valor"]
        urlMensaje = self.dsvApi+"mensajear"
        payload = {"ID":self.serie,"mensaje": fotobase64,"serie":self.serie,"tipo":tipo,"topico":self.topic,"valor":valor}
        r = requests.post(urlMensaje, json=payload).json()

      if mensaje["id"] == 7:
        print('GPIO:',mensaje["valor"])

      if mensaje["id"] == 8:
        print('Dron:',mensaje["valor"])
        tipo = mensaje["tipo"]
        urlMensaje = self.dsvApi+"mensajear"
        payload = {"ID":self.serie,"mensaje": "ON","serie":self.serie,"tipo":tipo,"topico":self.topicDronON,"valor":URLMQTT}
        r = requests.post(urlMensaje, json=payload).json()
      '''
    #print(r)
    #IMAGE = self.imagen
    #self.passw="walter"
    #self.username = "walter"
    #client_id=self.clientID, 
    #self.client = mqtt.Client()
    #self.client.username_pw_set(username=self.username,password=self.passw)
    #self.client.on_connect = self.ok()
    #self.client.connect(self.host, port=1883, keepalive=200)
    #self.client.publish("dsv/test","envio")
    #t1 =threading.Thread(name="enviar", target=self.publicar)
    #self.publicar(client)
    #t1.start()