import base64
import time
import boto3
import cv2
from imutils.object_detection import non_max_suppression
import numpy
import numpy as np
import paho.mqtt.client as mqtt

LOW_BANDWIDTH = True

broker = "104.238.164.118" # broker address
print("Connecting to broker...\n")
mqtt_client = mqtt.Client("client1") # client name
mqtt_client.connect(broker,8883,60) # broker, port, idklol

client = boto3.client(
	'rekognition',
	region_name='us-east-1',
	aws_access_key_id=open("../akey.txt").read().strip(),
	aws_secret_access_key=open("../skey.txt").read().strip(),

)

def getInfo(base64String):
	response = client.detect_labels(Image={'Bytes': base64String})
	return response

def detectInImage(listOfFeatures):
	listOfObjects = ["Coke", "Pepsi", "Drink", "Can", "Bottle"]
	for var in listOfObjects:
		if var.title() in listOfFeatures:
			return True
	return False

def isAGun(imageString):
	listOfFeatures = []
	for var in getInfo(imageString)['Labels']:
		listOfFeatures.append(var["Name"])
	return detectInImage(listOfFeatures)

def imgToNumpy(img):
	return numpy.array(cv2.imencode('.png', img)[1]).tostring()

while True:

	cap = cv2.VideoCapture(0)
	hog = cv2.HOGDescriptor()
	hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

	_,img = cap.read()

	# detect people in the image
	(rects, weights) = hog.detectMultiScale(img, winStride=(4, 4),
		padding=(8, 8), scale=1.05)
	for (x, y, w, h) in rects:
		cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

	# apply non-maxima suppression to the bounding boxes using a
	# fairly large overlap threshold to try to maintain overlapping
	# boxes that are still people
	rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
	pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
	if LOW_BANDWIDTH == True:
		if len(pick) != 0:
			isGun = isAGun(imgToNumpy(img))
		else:
			isGun = False
	else:
		isGun = isAGun(imgToNumpy(img))
	print isGun
	if (isGun == True):
		mqtt_client.publish("HP18/report", "ACTIVE SOFT DRINK ON PREMISES!") # sends warning
	cap.release()
	cv2.destroyAllWindows()
	mqtt_client.disconnect() # disconnects client
	time.sleep(.01)




#if __name__ == '__main__':

