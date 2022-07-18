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

class inicializarHands(object):
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
        self.model = tk.models.load_model("ai/conv/hands.h5")
        self.data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)  
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

    def stream(self, camera):
        #Por unica vez
        if self.ban == False:
            self.ban = True
        #Bucle    
        return camera

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

    def face_daemon(self, camera,gray,rgb):
        newImage = camera.copy()
        respuesta = ''
        '''
        results = self.pose.process(camera)
        if results.pose_landmarks:
            for id, lm in enumerate(results.pose_landmarks.landmark):
                if id == 17 or id == 18:
                    h, w, c = camera.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    startX = cx
                    startY = cy
                    endX = cx+5
                    endY = cy+1
                    color = (0,255,0)
                    p1 = startX-80,startY+40
                    p2 = endX+120,endY -100
                    #cv2.rectangle(camera, (p1),(p2),color,2)
                    roi_image = newImage[startY-100:endY+100,startX-100:endX+100]
                    h1, w1, _ = roi_image.shape

                    if id == 17:
                        pip_h = 10
                        pip_w = 10
                    if id == 18:
                        pip_h = 10
                        pip_w = 250                    
                    
                    #camera[pip_h:pip_h+h1,pip_w:pip_w+w1] = roi_image  # make it PIP

                    try:
                        self.main_tflow(roi_image,camera,startX+100,startY-100,p1,p2)
                    except:
                        pass        
        
        '''           

        img = self.detector.findPose(camera, draw = True)
        imgList, bboxInfo = self.detector.findPosition(img, draw = False)

        #imgList devuelve un array con 33 elementos y cada uno tiene un array de 3
        # el 17 y 18 son puntos de las manos

        if(len(imgList)> 0):
            color = (0,255,0)
            
            p1 = imgList[17][1]-80,imgList[17][2]+40
            p2 = imgList[17][1]+120,imgList[17][2]-100
            #cv2.rectangle(img, (p1),(p2),color,2)

            x1 = imgList[17][1]-20
            y1 = imgList[17][2]+40
            x2 = imgList[17][1]+40
            y2 = imgList[17][2]-10

            pip_h = 10
            pip_w = 250

            roi_image = newImage[y1-100:y2+100, x1-100:x2+100]
            h1, w1 = roi_image.shape[:2]
            #camera[pip_h:pip_h+h1,pip_w:pip_w+w1] = roi_image  # make it PIP 

            try:
                self.main_tflow(roi_image,camera,x1,y1,p1,p2)
            except:
                pass 
            
            p1 = imgList[18][1]-80,imgList[18][2]+40
            p2 = imgList[18][1]+120,imgList[18][2]-100
            #cv2.rectangle(img, (p1),(p2),color,2)

            x1 = imgList[18][1]-20
            y1 = imgList[18][2]+40
            x2 = imgList[18][1]+40
            y2 = imgList[18][2]-10
 
            pip_h = 10
            pip_w = 10

            roi_image = newImage[y1-100:y2+100, x1-100:x2+100]
            h1, w1 = roi_image.shape[:2]
            #camera[pip_h:pip_h+h1,pip_w:pip_w+w1] = roi_image  # make it PIP   

            #self.main_tflite(roi_image)
            try:
                self.main_tflow(roi_image,camera,x1,y1,p1,p2)
            except:
                pass 


        return camera

    def main_tflow(self,roi_image,camera,x1,y1,p1,p2):

        roi_image = cv2.resize(roi_image,(224,224))
        image_array=np.asarray(roi_image)
        normalize_image = (image_array.astype(np.float32) / 127.0) - 1


        self.data[0] = normalize_image
        prediction = self.model.predict(self.data)

        a = str(prediction[0][0])
        #b = str(prediction[0][1])
        #c = str(prediction[0][2])
        #d = prediction[0][3]
        #e = prediction[0][4]
        #e = prediction[0][4]

        #print(prediction)

        color = (28,0,255)

        label = ""
        #print(a[:7])
        if a[:7] == '0.99999':
            draw_strApe(camera, (x1 - 120, y1 + 25), f'Pistola: {a}',color)
            cv2.rectangle(camera, (p1),(p2),color,2)

        #elif b[:7] == '0.99999':
        #    draw_strApe(camera, (x1 - 50, y1 + 50), f'Cuchillo: {b}',color)
        #    cv2.rectangle(camera, (p1),(p2),color,2)
        #elif c[:7] == '0.99999':
        #    color = (0,255,0)
        #    draw_strApe(camera, (x1 - 50, y1 + 50), f' {c}',color)

        #elif d == 100:
        #    color = (0,255,0)
        #    draw_strApe(camera, (20, 200), f'Billetera: {d}',color)
        #elif e == 100:
        #    draw_strApe(camera, (x1 - 50, y1 + 50), f'Cuchillo: {e}',color)
        #    cv2.rectangle(camera, (p1),(p2),color,2)
        #elif f == 100:
        #    color = (0,255,0)
        #    draw_strApe(camera, (20, 200), f'Billete: {f}',color)            