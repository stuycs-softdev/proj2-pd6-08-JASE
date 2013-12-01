from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route("/")
def gmap(addr):
    a = addr.replace(" ","+")
    return "http://maps.googleapis.com/maps/api/staticmap?center="+a+"&zoom=13&size=600x300&maptype=roadmap&markers=color:red%7Clabel:A%7C"+a+"&sensor=false"
#    return "maps.googleapis.com/maps/api/staticmap?center=" + addr + "&markers=color:blue%7Clabel:C%7C" + addr + "&zoom=16&size=640x640&sensor=false&key=AIzaSyAEH1zvTqgnRGLX8WIerdMnjZiB2Scyys0"


#maps.googleapis.com/maps/api/staticmap?center={{addr}}&markers=color:blue%7Clabel:C%7C{{addr}}&zoom=16&size=640x640&sensor=false
if __name__ == "__main__":
    addr = raw_input("Enter address: ")
    zipc = raw_input("Enter zip code: ")
    data = gmap(addr,zipc)
    print("maps.googleapis.com/maps/api/staticmap?center=" + addr + " " + zip + "&markers=color:blue%7Clabel:C%7C" + addr + " " + zip + "&zoom=16&size=640x640&sensor=false&key=AIzaSyAEH1zvTqgnRGLX8WIerdMnjZiB2Scyys0")
