import base64

import boto3
client = boto3.client(
	'rekognition',
	region_name='us-east-1',
	aws_access_key_id=open("../akey.txt").read().strip(),
	aws_secret_access_key=open("../skey.txt").read().strip(),

)

def getEmotion(base64String):
	response = client.detect_labels(Image={'Bytes': base64String})
	return response

if __name__ == '__main__':
	listOfFeatures = []
	sourceBytes = open("test.png", "rb").read()
	for var in getEmotion(sourceBytes)['Labels']:
		listOfFeatures.append(var["Name"])
	print listOfFeatures
