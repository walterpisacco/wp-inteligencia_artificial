from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import io
import time
import numpy as np
import imutils
#pip install opencv-python
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
import face_recognition

from config import config
configuracion = config()

global client
global frameid
frameid = 0
global URLMQTT
URLMQTT = ''
 
class inicializarFace(object):
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
        self.detector = cv2.CascadeClassifier(configuracion.pathModelos+'haarcascade_frontalface_default.xml')
   
  def get_frame(self):
      #opcion del select filterInput (opciones deltro del txt seleccionado)
      opcion  = self.opcion
      iot     = self.iot
      success, self.frame = self.video.read()

      frameOriginal = imutils.resize(self.frame, width=720)

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
    
    rects = self.detector.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=6, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
    
    color = (0, 255, 0)
    
    for (x,y,w,h) in rects:
      p1 = x-10,y-10
      p2 = x+w+10,y+h+10
      #cv2.rectangle(frameOriginal, (p1),(p2),color,2)
      #draw_strApe(frameOriginal, (400, 70), 'Identificando...',color)
    

    #boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
    #encodings = face_recognition.face_encodings(frame, boxes)
    #for encoding in encodings:
    #  print(rects)
    #  draw_rects(frame, rects, (0, 255, 0))

    return frameOriginal

