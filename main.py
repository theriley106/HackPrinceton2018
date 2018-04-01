#!/usr/bin/env python3
import base64
import lib
import time
import os
import boto3
import cv2
from imutils.object_detection import non_max_suppression
import numpy
import numpy as np
import paho.mqtt.client as mqtt

LOW_BANDWIDTH = True

print("Connecting to broker...\n")
mqtt_client = mqtt.Client("client1") # new client with name
mqtt_client.connect("104.238.164.118", 8883, 60) # connects to broker address

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
	listOfObjects = ["Hardware", "Power Drill", "Drill", "Electronics"]
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

def sendText(number, text="Emergency Situation Detected at {0}", location="Princeton University"):
	text = text.format(location)

	# You should avoid sharing this token,
	#  and should store it in an env variable
	lib = lib(token=open("../libKey.txt").read())
sms = lib.messagebird.sms["@0.1.3"]

result = sms.create(
  recipient="18645674106", # (required)
  body="Testing to see if this works" # (required)
)


if __name__ == '__main__':
	while True:

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
		if isGun == True:
			mqtt_client.publish("HP18/report/test", "SEND TEST raspi")
		cap.release()
		cv2.destroyAllWindows()
		mqtt_client.disconnect() # disconnects client from broker
		time.sleep(.01)






