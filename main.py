import base64

import boto3
client = boto3.client(
	'rekognition',
	region_name='us-east-1',
	aws_access_key_id=open("../akey.txt").read().strip(),
	aws_secret_access_key=open("../skey.txt").read().strip(),

)
# Set this to whatever percentage of 'similarity'
# you'd want
SIMILARITY_THRESHOLD = 75.0

def getEmotion(base64String):
	response = client.detect_labels(Image={'Bytes': base64String})
	return response

if __name__ == '__main__':
	sourceBytes = open("test.png", "rb").read()

	print getEmotion(sourceBytes)
