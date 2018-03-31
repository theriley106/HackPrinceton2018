#!/usr/bin/env python3
import io
import picamera
import base64
import time
import os
import boto3
import cv2
from imutils.object_detection import non_max_suppression
import numpy
import numpy as np
import paho.mqtt.client as mqtt
from PIL import Image
import io
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
#camera = picamera.PiCamera()
#stream = io.BytesIO()

'''while True:
	camera.capture(stream, 'png')
	img = Image.open(stream)
	isGun = isAGun(imgToNumpy(img))
	if isGun == True:
		#os.system("python talk.py")
		mqtt_client.publish("HP18/report", "ACTIVE SOFT DRINK ON PREMISES!") # sends warning

	mqtt_client.disconnect() # disconnects client
	time.sleep(.01)'''
while True:
	# Create the in-memory stream
	stream = io.BytesIO()
	camera = picamera.PiCamera()
	camera.start_preview()
	time.sleep(1)
	camera.capture(stream, format='png')
	# "Rewind" the stream to the beginning so we can read its content
	stream.seek(0)
	image = Image.open(stream)
	isGun = isAGun(base64.encodestring(image))




#if __name__ == '__main__':

