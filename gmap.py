from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route("/")
def gmap():
	if request.method=="GET":
		return render_template("index.html")
	else:
		button = request.form['button']
		if button=="Submit":
			address = request.form['address']
			return render_template("map.html",addr=address)
		else:
			return render_template("index.html")

if __name__=="__main__":
	app.debug=True
	app.run(host="0.0.0.0",port=5000)
