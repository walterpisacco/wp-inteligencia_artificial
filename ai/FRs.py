import numpy as np
import imutils
import cv2
import os
import json
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import pickle
import threading
import time
import paho.mqtt.client as mqtt

#from alarma import alarm
from datetime import datetime

#pip install vidgear
from vidgear.gears import CamGear
from gtts import gTTS
from playsound import playsound

#import RPi.GPIO as GPIO

from common import clock, draw_str, draw_strApe, draw_rects, overlay_transparent, draw_rectangulo

class inicializarFRs(object):
    def __init__(self, camara='0',webcamId='0',serie='',tipo='',label='',modelo='',opcion='',iot='',dsvApi=''):
        self.labels=label #Cargo las etiquetas
        self.modelo = modelo
        self.serie = serie
        self.tipo = tipo
        self.opcion = opcion
        self.iot = iot
        self.dsvApi = dsvApi  
        self.detector = cv2.CascadeClassifier('ai/conv/haarcascade_frontalface_alt.xml')
        self.data = pickle.loads(open(self.modelo, "rb").read())
        self.ban = False #Bandera Para que cargue una sola Vez el Modelo YOLO
        self.mqtt = mqtt.Client()
        self.webcamId = int(webcamId)

        if int(webcamId) < 5:
            self.video = cv2.VideoCapture(int(camara))
        elif int(webcamId) ==5:
            self.video = cv2.VideoCapture('ai/conv/'+camara)
        elif int(webcamId) ==6:
            url   = camara
            self.video = CamGear(source=url, stream_mode = True, logging=True).start() # YouTube Video URL        
    
    def __del__(self):
        self.video.release()

    def get_frame(self):
        # para link de youtube
        if(self.webcamId ==6):
            image = self.video.read()

        #para el resto de los videos
        if(self.webcamId !=6):
            success, image = self.video.read()

        image = imutils.resize(image, width=1280)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        marco = self.face_daemon(image, gray, rgb)
        ret, jpeg = cv2.imencode('.jpg', marco)
        return jpeg.tobytes()

    def detener_frame(self):
        self.video.release()
        print("borrado")

    def get_img(self):
        success, frame = self.video.read()
        if success:
            image = frame
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            marco = self.face_daemon(image, gray, rgb)
            
            return marco
        else:
            print ("Error al obtener imagen (comprobar RTSP o WEBCAM)")
            time.sleep(10)

    def face_daemon(self, camera,gray,rgb):
        rects = self.detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
        
        color = (255, 255, 255)
        for (x,y,w,h) in rects:
            p1 = x-10,y-10
            p2 = x+w+10,y+h+10
            cv2.rectangle(camera, (p1),(p2),color,2)
            draw_str(camera, (400, 70), 'Identificando...',color,2,1)

        boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
        
        encodings = face_recognition.face_encodings(rgb, boxes)
        names = []        

        for encoding in encodings: 
            matches = face_recognition.compare_faces(self.data["encodings"],encoding,tolerance=0.5)
            name = "Desconocido"      
         
            color = (0, 255, 0)
            
            if True in matches:
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}
              
                for i in matchedIdxs:
                    name = self.data["names"][i]
                    counts[name] = counts.get(name, 0) + 1
                
                name = max(counts, key=counts.get)

                ##########################dibuja cuadro###########################
                overlay = cv2.imread('static/graph/ventana.png', cv2.IMREAD_UNCHANGED)
                overlay = cv2.resize(overlay, (350,120))
                overlay_transparent(camera, overlay, 1, 1)

                color = (0, 255, 0)
                draw_str(camera, (45, 70), name.upper(),color,2,1)

                tts = gTTS('Persona identificada, '+name, lang='es-es', slow=False)
                NOMBRE_ARCHIVO = name+".mp3"
                with open(NOMBRE_ARCHIVO, "wb") as archivo:
                    tts.write_to_fp(archivo)

                playsound(NOMBRE_ARCHIVO)

            else:
                color = (0, 255, 0)
                
            cv2.rectangle(camera, (p1),(p2),color,2)
    
            names.append(name)
            if name!="Desconocido":
                if self.ban == False:
                    print(name)
                    try:
                        print("Envio a MQTT platform.drexgen.com")
                        self.mqtt.username_pw_set(username="admin", password="global*3522")
                        self.mqtt.connect("platform.drexgen.com", 1883, 60)
                        self.mqtt.publish("cmnd/010101/onoff/POWER",'on')
                        self.mqtt.publish("dsv/seg/od/R00001PI04V0001/DPublica5",'{"serie":"R00001PI04V0001","posx":"356.9709307059686","posy":"226"}')
                    except:
                        print("No conecta con MQTT platform.drexgen.com")
                    #self.send_api()
                    self.encender(self.ban)
                    timer = threading.Timer(5.0, self.encender)
                    timer.start()
                    #alarm.send_mqtt(name, camera)
                    self.ban = True
 
            else:
                self.ban = False
                
        
        for ((top, right, bottom, left), name) in zip(boxes, names):
            pass

        return camera
    
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
          self.ban=False

