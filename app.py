import sys
reload(sys)
sys.setdefaultencoding('UTF8')
from flask import Flask, request, jsonify, render_template, request, url_for, redirect, Markup, Response, send_file, send_from_directory, make_response
app = Flask(__name__,template_folder="templates/",static_url_path='/static')


@app.route('/')
def main():
	return render_template('index.html')

if __name__ == "__main__":
	app.run(host='0.0.0.0')
