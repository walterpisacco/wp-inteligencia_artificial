#python entrenador.py -n nombre
import cv2
import os
import argparse
import imutils


ap = argparse.ArgumentParser()
ap.add_argument("-n", "--name", required=True,
	help="path to input directory of faces + images")
args = vars(ap.parse_args())


if not os.path.exists(f'dataset/{args["name"]}'):
	print('Carpeta creada: dataset')
	os.makedirs(f'dataset/{args["name"]}')

ruta = f'dataset/{args["name"]}/{args["name"]}_'
print (ruta)

cap = cv2.VideoCapture(0)

faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

count = 0
while True:
	ret,frame = cap.read()
	frame = cv2.flip(frame,1)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	auxFrame = frame.copy()
	frame2 = frame.copy()

	faces = faceClassif.detectMultiScale(gray, 1.3, 5)

	k = cv2.waitKey(1)
	if k == 27:
		break

	for (x,y,w,h) in faces:
		p1 = x-50,y-50
		p2 = x+w+50,y+h+50
		cv2.rectangle(frame, (p1),(p2),(128,0,255),2)
		#rostro = auxFrame[y:y+h,x:x+w]
		rostro = auxFrame[y-50:y+h+50,x-50:x+w+50]
		rostro = cv2.resize(rostro,(150,150), interpolation=cv2.INTER_CUBIC)
		#cv2.imshow('rostro',rostro)
		if k == ord('s'):
			cv2.imwrite('{}_{}.jpg'.format(ruta,count),frame2)
			cv2.imshow('rostro',rostro)
			count = count +1
	
	cv2.rectangle(frame,(10,5),(450,25),(255,255,255),-1)
	cv2.putText(frame,'Presione s, para almacenar los rostros encontrados',(10,20), 2, 0.5,(128,0,255),1,cv2.LINE_AA)
	cv2.imshow('frame',frame)

cap.release()
cv2.destroyAllWindows()
