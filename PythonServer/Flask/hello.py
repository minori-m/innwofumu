# python

from flask import Flask

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
	return "Hello"

if __name__ == "__main__":
	app.debug = True
	app.run()