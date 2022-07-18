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

#pip install RPi.GPIO
#from gpio import gpio

#from graf.common import clock, draw_str, draw_strApe, draw_rects, overlay_transparent

global client
global frameid
frameid = 0


class ident(object):
  def __init__(self, serie='',label='',modelo='',opcion='',iot=''):
        self.LABELS=label #Cargo las etiquetas
        self.MODEL = modelo
        self.serie = serie
        self.opcion = opcion
        self.interpreter = None       
        #self.input_cam = (camara) #indice de la Camara o rtsp
        #self.video = cv2.VideoCapture(self.input_cam) #Cap de la camara
        self.ban = False #Bandera Para que cargue una sola Vez el Modelo YOLO
        self.labels = None #Donde Se carga el Detector
        self.ban1 = False
        self.conf = 0.9
        self.anchoSalida = 400
        self.altoSalida = 320
        self.anchoAnalisis = 224
        self.altoAnalisis = 224        
        

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


  def main_tflite(self,matriz):
    print(self.MODEL)
    #with open(self.LABELS, 'r') as f:
    #  self.labels = {i: line.strip() for i, line in enumerate(f.readlines())}
    self.interpreter = Interpreter(self.MODEL)
    self.interpreter.allocate_tensors()
    _, height, width, _ = self.interpreter.get_input_details()[0]['shape']
    
    
    #overlay = cv2.imread('static/graph/ventana.png', cv2.IMREAD_UNCHANGED)
    #overlay = cv2.resize(overlay, (180,60))
    #overlay_transparent(frameOriginal, overlay, 5, 5)

    image_array = np.asarray(matriz)
    image_array = cv2.resize(image_array,(224,224))
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    start_time = time.time()
    results = self.classify_image(self.interpreter, normalized_image_array)
    print (results)
    elapsed_ms = (time.time() - start_time) * 1000
    #text = self.labels[results[0][0]]
    #text = text.split (" ")

    #if(int(text[0]) == int(opcion) and int(iot) == 1):
    #  if self.ban1 == False:
    #    print('SUENA ALARMA!!')
    #    print ("true")
    #    #self.gpio.upin()
    #    self.ban1 = True
    #  elif (int(text[0]) == int(opcion) and int(iot) == 0):
    #    self.ban1 = False
#
    #texto = text[1]

    #if(int(text[0]) == 0):
    #  color = (0, 160, 255)
    #else:
    #  color = (0, 0, 255)

    #draw_strApe(frameOriginal, (20, 40), texto,color) 
    #return frameOriginal
    #return text[1]
    return results

