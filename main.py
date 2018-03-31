import base64

import boto3
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

if __name__ == '__main__':
	listOfFeatures = []
	sourceBytes = open("test.png", "rb").read()
	for var in getInfo(sourceBytes)['Labels']:
		listOfFeatures.append(var["Name"])
	print detectInImage(listOfFeatures)
