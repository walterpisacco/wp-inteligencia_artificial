import pytesseract
from PIL import Image

#pip3 install mediapipe
#pip install opencv-python-headless==4.5.2.52

from cvzone.PoseModule import PoseDetector
import numpy as np
import cv2
from imutils.video import VideoStream
from imutils.video import FPS
import time
import paho.mqtt.client as mqtt
#pip install mediapipe
#pip install mediapipe-rpi4 PARA RASPI
import mediapipe as mp
import imutils
from tflite_runtime.interpreter  import Interpreter

import tensorflow.keras as tk

#pip install youtube-dl
#pip install vidgear
from vidgear.gears import CamGear

#import RPi.GPIO as GPIO

from gtts import gTTS
from playsound import playsound

from common import clock, draw_str, draw_strApe, draw_rects, overlay_transparent, draw_rectangulo

class inicializarALPR(object):
    def __init__(self, camara='0',webcamId = 0,serie='',tipo='',label='',modelo='',opcion='',iot='',dsvApi=''):
        self.LABELS=label #Cargo las etiquetas
        self.labels=label #Cargo las etiquetas
        self.MODEL = modelo
        self.modelo = modelo
        self.serie = serie
        self.tipo = tipo
        self.opcion = opcion
        self.iot = iot
        self.dsvApi = dsvApi
        self.input_cam = camara #indice de la Camara
        self.ban = False #Bandera Para que cargue una sola Vez el Modelo YOLO
        self.mqtt = mqtt.Client()
        self.interpreter = None 
        self.ban = False #Bandera Para que cargue una sola Vez el Modelo YOLO
        self.anchoAnalisis = 224
        self.altoAnalisis = 224
        self.webcamId = int(webcamId)

        if int(webcamId) < 5:
            self.video = cv2.VideoCapture(int(camara))
        elif int(webcamId) ==5:
            self.video = cv2.VideoCapture('ai/conv/'+camara)
        elif int(webcamId) ==6:
            url   = camara
            self.video = CamGear(source=url, stream_mode = True, logging=True).start() # YouTube Video URL

        np.set_printoptions(suppress=True)
        self.patenteAnt = ''
        self.patenteCant = 0

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
        marco = self.video_daemon(image, gray, rgb)
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
            marco = self.video_daemon(image, gray, rgb)
            
            return marco
        else:
            print ("Error al obtener imagen (comprobar RTSP o WEBCAM)")
            time.sleep(10)

    def video_daemon(self, camera,gray,rgb):
        camera = imutils.resize(camera, width=720)
        gray = cv2.cvtColor(camera, cv2.COLOR_BGR2GRAY) #convert to grey scale
        gray = cv2.bilateralFilter(gray, 11, 17, 17) #Blur to reduce noise
        edged = cv2.Canny(gray, 30, 200) #Perform Edge detection

        try:
            # find contours in the edged image, keep only the largest
            # ones, and initialize our screen contour
            cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
            screenCnt = None

            ##########################dibuja cuadro###########################

            # loop over our contours
            for c in cnts:
             # approximate the contour
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.018 * peri, True)
             
             # if our approximated contour has four points, then
             # we can assume that we have found our screen
                if len(approx) == 4:
                    screenCnt = approx
                break

            if screenCnt is None:
                detected = 0
            else:
                detected = 1

            if detected == 1:
                cv2.drawContours(camera, [screenCnt], -1, (0, 255, 0), 3)
                #cv2.drawContours(camera, [screenCnt.astype(int)], 0, (255, 0, 0), 3)

                # Masking the part other than the number plate
                mask = np.zeros(gray.shape,np.uint8)
                new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)
                #new_image = cv2.drawContours(mask, [screenCnt.astype(int)], 0, (255, 0, 0), 3)
                new_image = cv2.bitwise_and(camera,camera,mask=mask)

                #Now crop
                (x, y) = np.where(mask == 255)
                (topx, topy) = (np.min(x), np.min(y))
                (bottomx, bottomy) = (np.max(x), np.max(y))
                Cropped = gray[topx:bottomx+1, topy:bottomy+1]

                #Read the number plate
                text = pytesseract.image_to_string(Cropped, config='--psm 10 --oem 1 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
                text = text.replace('\n','',4) # quitar enters
                text = text.strip() # quitar enters al inicio y final
                patente = text

                #if len(text) == 6:
                #    print("Detected Number is:",text)
                #    overlay = cv2.imread('static/graph/patente2.png', cv2.IMREAD_UNCHANGED)
                #    overlay = cv2.resize(overlay, (200,70))
                #    overlay_transparent(camera, overlay, 1, 1)
                #    text = text[:3] + ' ' + text[-3:]
                #    color = (255, 255, 255)
                #    draw_str(camera,  (20, 55), text[-7:],color,2,2)

                if len(text) == 7:
                    overlay = cv2.imread('static/graph/patente1.png', cv2.IMREAD_UNCHANGED)
                    overlay = cv2.resize(overlay, (200,70))
                    overlay_transparent(camera, overlay, 1, 1)  
                    text = text[:2] + ' ' + text[2:5] + ' ' + text[-2:]
                    color = (0, 0, 0)
                    draw_str(camera,  (20, 55), text[-9:],color,2,2)                  
                    print("Patente: ",patente)

                    if self.patenteAnt != patente:
                            self.patenteAnt = patente
                            self.patenteCant = 1            

                    if self.patenteCant == 5:
                        try:
                            tts = gTTS('Patente, '+patente, lang='es-es', slow=False)
                            NOMBRE_ARCHIVO = patente+".mp3"
                            with open(NOMBRE_ARCHIVO, "wb") as archivo:
                                tts.write_to_fp(archivo)

                            playsound(NOMBRE_ARCHIVO)
                            
                            print("Envio a MQTT")
                            self.mqtt.username_pw_set(username="", password="")
                            self.mqtt.connect("", 1883, 60)
                            self.mqtt.publish("dsv/seg/alpr/32CE115044/alerta/DPublica1",'{"ID": "32CE115044", "Date": "2022-05-20 16:00:39","Pais":"Argentina", "Marca": "volkswagen", "Modelo": "fiat_strada", "Fecha": "2005-2009", "Color": "white", "Tipo": "truck-standard", "Patente": "'+patente+'"}')
                            print("Patente nueva: ",patente)

                            self.patenteCant = 1
                        except:
                            print("No conecta con MQTT")
                    else:
                        self.patenteCant = self.patenteCant + 1

        except:
            pass 
            
        return camera

        #dsv/seg/alpr/32CE115044/alerta/DPublica1
        #{"ID": "32CE115044", "Date": "2022-05-20 16:00:39","Pais":"Argentina", "Marca": "volkswagen", "Modelo": "fiat_strada", "Fecha": "2005-2009", "Color": "white", "Tipo": "truck-standard", "Patente": "AG759LH"}
