import requests
import shutil
import threading
import main
import time
import app

URLs = ['http://10.24.88.66/html/cam_pic.php?time=12', "http://10.25.213.197/cam_pic.php?time=0"]

def checkForGun(url):
	prevAns = False
	while True:
		try:
			print("Checking {}".format(url))
			response = requests.get(url, stream=True)
			with open('file{}.png'.format(URLs.index(url)), 'wb') as out_file:
				shutil.copyfileobj(response.raw, out_file)
			del response
			with open("file{}.png".format(URLs.index(url)), "rb") as f:
				data = f.read()
			isGun, labels = main.isAGunWFeatures(data)
			if isGun == True and prevAns == True:
				app.raiseIssue(URLs.index(url), labels)
				print("BLAH BLAH {}".format(URLs.index(url)))
			prevAns = isGun
		except Exception as exp:
			print exp
		time.sleep(.5)


threads = [threading.Thread(target=checkForGun, args=(url,)) for url in URLs]
for thread in threads:
	thread.start()

for thread in threads:
	thread.join()
