import requests
import shutil
import threading

URLs = ['http://10.24.88.66/html/cam_pic.php?time=12', "http://10.25.213.197/cam_pic.php?time=0"]

def checkForGun(url):
	while True:
		response = requests.get(url, stream=True)
		with open('file.png', 'wb') as out_file:
		    shutil.copyfileobj(response.raw, out_file)
		del response
		with open("file.png", "rb") as f:
	   		data = f.read()
	   	isGun = isAGun(data)
		print isGun


url = 'http://10.24.88.66/html/cam_pic.php?time=12'
	response = requests.get(url, stream=True)
	with open('file.png', 'wb') as out_file:
	    shutil.copyfileobj(response.raw, out_file)
	del response
	with open("file.png", "rb") as f:
   		data = f.read()
   	isGun = isAGun(data)
	print isGun
