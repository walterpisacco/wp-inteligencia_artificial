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

from common import clock, draw_str, draw_strApe, draw_rects, overlay_transparent, draw_rectangulo

class inicializarH5(object):
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
        self.detector = PoseDetector()
        self.input_cam = camara #indice de la Camara
        self.ban = False #Bandera Para que cargue una sola Vez el Modelo YOLO
        self.mqtt = mqtt.Client()
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose()
        self.interpreter = None 
        self.ban = False #Bandera Para que cargue una sola Vez el Modelo YOLO
        self.anchoAnalisis = 224
        self.altoAnalisis = 224
        self.model = tk.models.load_model(modelo)
        self.data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)  
        self.webcamId = int(webcamId)

        if int(webcamId) < 5:
            self.video = cv2.VideoCapture(int(camara))
        elif int(webcamId) ==5:
            self.video = cv2.VideoCapture('ai/conv/'+camara)
        elif int(webcamId) ==6:
            url   = camara
            self.video = CamGear(source=url, stream_mode = True, logging=True).start() # YouTube Video URL

        np.set_printoptions(suppress=True)

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

    def set_input_tensor(self,interpreter, image):
        tensor_index = interpreter.get_input_details()[0]['index']
        input_tensor = interpreter.tensor(tensor_index)()[0]
        input_tensor[:, :] = image

    def video_daemon(self, camera,gray,rgb):
        size = (224, 224)
        frame = cv2.resize(camera, size)
        camera = imutils.resize(camera, width=720)
        ###################################
        image_array = np.asarray(frame)
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

        self.data[0] = normalized_image_array
        prediction = self.model.predict(self.data)

        a = prediction[0][0] * 100
        b = prediction[0][1] * 100

        label = "No detecta"
        color = (0, 0, 255)
        if a > 80:
            label = f'LLeno'
            prec = f'Prec: {a}'
            color = (0, 255, 0)
        elif b > 70:
            label = f'Vacio'
            prec = f'Prec: {a}'
            color = (255, 153, 51)

        size = (400, 300)

        ##########################dibuja cuadro###########################
        overlay = cv2.imread('static/graph/ventana.png', cv2.IMREAD_UNCHANGED)
        overlay = cv2.resize(overlay, (200,70))
        overlay_transparent(camera, overlay, 1, 1)

        prec = str(prec)[5:13]
        draw_str(camera,  (20, 40), label,color,1,1)
        draw_str(camera,  (70, 40), prec,color,1,1)   
            
        return camera

