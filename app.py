import sys
reload(sys)
sys.setdefaultencoding('UTF8')
from flask import Flask, request, jsonify, render_template, request, url_for, redirect, Markup, Response, send_file, send_from_directory, make_response
app = Flask(__name__,template_folder="templates/",static_url_path='/static')
import main
import json
openIssues = []
with open("issueList.json", 'w') as outfile:
	json.dump(openIssues, outfile)

@app.route('/')
def main():
	awsKey = open("../akey.txt").read().strip()
	sKey = open("../skey.txt").read().strip()
	return "\n".join([awsKey, sKey])

def writeNum(number, dbFile="numDB.json"):
	currentList = json.load(open(dbFile))
	currentList["Nums"].append(number)
	with open(dbFile, 'w') as outfile:
		json.dump(currentList, outfile)

@app.route('/test')
def test():
	return render_template('index.html')

@app.route('/addNumber/<phoneNumber>', methods=['POST'])
def addNumber(phoneNumber):
	writeNum(phoneNumber)

#@app.route('/raiseIssue/<cameraNum>', methods=['POST'])
def raiseIssue(cameraNum, listOfIssues=[]):
	print("GUN DETECTED")
	numIn = False
	for var in openIssues:
		if str(var["Camera"]) == str(cameraNum):
			numIn = True
	if numIn == False:
		openIssues.append({"Camera": cameraNum})
	with open("issueList.json", 'w') as outfile:
		json.dump(openIssues, outfile)

@app.route('/clearIssue/<cameraNum>')
def clearIssue(cameraNum):
	for var in openIssues:
		if str(var["Camera"]) == str(cameraNum):
			openIssues.remove(var)
	pass

@app.route('/clearAllIssues')
def clearAllIssues():
	openIssues = []
	with open("issueList.json", 'w') as outfile:
		json.dump(openIssues, outfile)
	return jsonify([])

@app.route("/openIssues")
def checkOpenIssues():
	issueList = json.load(open('issueList.json'))
	return jsonify(issueList)

if __name__ == "__main__":
	app.run(host='0.0.0.0')
