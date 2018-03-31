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
import cStringIO

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



camera = picamera.PiCamera()
while True:
	# Create the in-memory stream
	camera.capture('file.png')
	with open("file.png", "rb") as f:
   		data = f.read()
	isGun = isAGun(data)
	print isGun
	if isGun == True:
		mqtt_client.publish("HP18/report/test", "SEND TEST raspi")
	time.sleep(.1)
