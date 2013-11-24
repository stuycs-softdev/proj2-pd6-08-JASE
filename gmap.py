from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route("/")
def gmap(addr,zipc):
    c = MongoClient()
    addr = "maps.googleapis.com/maps/api/staticmap?center=" + addr + " " + zip + "&markers=color:blue%7Clabel:C%7C" + addr + " " + zip + "&zoom=16&size=640x640&sensor=false&key=AIzaSyAEH1zvTqgnRGLX8WIerdMnjZiB2Scyys0"
    for x in range(0,len(teachers)):
        teachers[x]["address"] = x
        c.teachers.Collections.insert(addr[x])

#maps.googleapis.com/maps/api/staticmap?center={{addr}}&markers=color:blue%7Clabel:C%7C{{addr}}&zoom=16&size=640x640&sensor=false
if __name__ == "__main__":
    addr = raw_input("Enter address: ")
    zipc = raw_input("Enter zip code: ")
    data = gmap(addr,zipc)
    print("maps.googleapis.com/maps/api/staticmap?center=" + addr + " " + zip + "&markers=color:blue%7Clabel:C%7C" + addr + " " + zip + "&zoom=16&size=640x640&sensor=false&key=AIzaSyAEH1zvTqgnRGLX8WIerdMnjZiB2Scyys0")
