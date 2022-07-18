

# python3 encode_faces.py --dataset dataset --encodings encodings/encodings.pickle --detection-method cnn
# Raspberry Pi (faster, more accurate):
# python3 encode_faces.py --dataset dataset --encodings encodings.pickle --detection-method hog


from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os


#tipo de modelo
CNN = "cnn"

print("[INFO] quantifying faces...")
imagePaths = list(paths.list_images('dataset'))

knownEncodings = []
knownNames = []

for (i, imagePath) in enumerate(imagePaths):

	print("[INFO] processing image {}/{}".format(i + 1,
		len(imagePaths)))
	name = imagePath.split(os.path.sep)[-2]


	image = cv2.imread(imagePath)
	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


	boxes = face_recognition.face_locations(rgb,
		model=CNN)


	encodings = face_recognition.face_encodings(rgb, boxes)


	for encoding in encodings:

		knownEncodings.append(encoding)
		knownNames.append(name)


print("[INFO] serializing encodings...")
data = {"encodings": knownEncodings, "names": knownNames}
print (data)
f = open('ai/conv/faces.pickle', "wb")
f.write(pickle.dumps(data))
f.close()