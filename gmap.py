from flask import Flask

app = Flask(__name__)

@app.route("/")
def gmap(addr):
    c = MongoClient()
    addr = "maps.googleapis.com/maps/api/staticmap?center=" + addr + "&markers=color:blue%7Clabel:C%7C" + addr + " " + zip + "&zoom=16&size=640x640&sensor=false&key=AIzaSyAEG1zvTqgnTHLX8WIerdMnjZiB2Scyys0"
    for x in range(0,len(tea):
        teachers[x]["address"] = x
        c.teachers.Collections.insert(addr[x])

#maps.googleapis.com/maps/api/staticmap?center={{addr}}&markers=color:blue%7Clabel:C%7C{{addr}}&zoom=16&size=640x640&sensor=false
if __name__ == "__main__":
    addr = raw_input("Enter address: ")
    data = gmap(addr);
    
