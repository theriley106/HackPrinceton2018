import requests
import shutil
import threading
import main

URLs = ['http://10.24.88.66/html/cam_pic.php?time=12', "http://10.25.213.197/cam_pic.php?time=0"]

def checkForGun(url):
	while True:
		print("Checking {}".format(url))
		response = requests.get(url, stream=True)
		with open('file{}.png'.format(URLs.index(url)), 'wb') as out_file:
		    shutil.copyfileobj(response.raw, out_file)
		del response
		with open("file{}.png".format(URLs.index(url)), "rb") as f:
	   		data = f.read()
	   	isGun = isAGun(data)
	   	if isGun == True:
	   		main.setAlarm(url)


threads = [threading.Thread(target=chekForGun, args=(url,)) for url in URLs]
for thread in threads:
	thread.start()

for thread in threads:
	thread.join()
