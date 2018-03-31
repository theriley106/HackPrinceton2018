import base64
import time
import boto3
import cv2
import numpy


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


while True:
	cap = cv2.VideoCapture(0)
	listOfFeatures = []
	_,img = cap.read()
	a = numpy.array(cv2.imencode('.png', img)[1]).tostring()
	for var in getInfo(a)['Labels']:
		listOfFeatures.append(var["Name"])
	if detectInImage(listOfFeatures):
		print("\"Gun\" Has Been Detected")
	else:
		print("No Gun")
	cap.release()
	cv2.destroyAllWindows()
	time.sleep(.01)





#if __name__ == '__main__':

