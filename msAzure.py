import requests



if __name__ == '__main__':
	subscription_key = open("../mkey.txt").read().strip()
	image_url = 'https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/images/family_photo.jpg'
	vision_analyze_url = 'https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/analyze'
	headers  = {'Ocp-Apim-Subscription-Key': subscription_key }
	params   = {'visualFeatures': 'Categories,Description,Color'}
	data     = {'url': image_url}
	response = requests.post(vision_analyze_url, headers=headers, params=params, json=data)
	response.raise_for_status()
	analysis = response.json()
	print analysis
