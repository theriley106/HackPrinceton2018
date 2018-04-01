import base64
import requests
url = 'http://10.24.88.66/html/cam_pic.php?time=12'
response = requests.get(url)
uri = ("data:" +
       response.headers['Content-Type'] + ";" +
       "base64," + base64.b64encode(response.content))
