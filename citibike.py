
import time
import urllib2
import json
import math
from pymongo import MongoClient



def getDocks():
    url = 'http://citibikenyc.com/stations/json'


    result = urllib2.urlopen(url)


    r = []
    k = json.loads(result.read())["stationBeanList"]
    
    for x in k:
        r.append({
                "lat":x["latitude"],
                "long":x["longitude"],
                "name":x["stationName"]
                })
        

    return r



def closest(lat,lng,docks=False):
    if docks == False:
        docks = getDocks()

    closest = -1
    closestDist = -1

    for y in range(0,len(docks)):
        x = docks[y]
        d = math.sqrt(math.pow(x["lat"]-lat,2)+math.pow(x["long"]-lng,2))
        
        if closestDist == -1 or d < closestDist:
            closest = y
            closestDist = d

    return docks[closest]



def getBikeRoute(a,b):
    url = "http://maps.googleapis.com/maps/api/directions/json?origin=%s,%s&destination=Stuyvesant+High+School&sensor=false&mode=bicycling&arrival_time=47000"%(str(a),str(b))
    
    result = urllib2.urlopen(url)

    try:
        k = json.loads(result.read())

        if k["status"] == "OVER_QUERY_LIMIT":
            time.sleep(2)
            return getBikeRoute(a,b)

        return k
    except:
        if result.read().lstrip() == "":
            time.sleep(2)
            return getBikeRoute(a,b)
        return None


def getWalkingRoute(a,b):
    url = "http://maps.googleapis.com/maps/api/directions/json?origin=%s,%s&destination=%s,%s&sensor=false&mode=walking&arrival_time=47000"%(str(a[0]),str(a[1]),str(b[0]),str(b[1]))
    
    result = urllib2.urlopen(url)

    try:
        k = json.loads(result.read())

        if k["status"] == "OVER_QUERY_LIMIT":
            time.sleep(3)
            return getWalkingRoute(a,b)
        
        return k

    except:
        return None



def updateTeachers():
    # only do this for teachers that live in Manhattan or Brooklyn
    docks = getDocks()

    c = MongoClient()

    for x in c.teachers.Collections.find().sort("last"):
        if len(x["address"]) > 0 and "lat" in x["address"][0].keys() and ("New York" in x["address"][0]["address"] or "Brooklyn" in x["address"][0]["address"]):

            clos = closest(x["address"][0]["lat"],x["address"][0]["long"],docks)
            a = getBikeRoute(clos["lat"],clos["long"])
            b = getWalkingRoute([x["address"][0]["lat"],x["address"][0]["long"]],
                                [clos["lat"],clos["long"]])
    
            if a != None and b != None:
                print("%s %s: %s - %s"%(x['first'],x['last'],x['address'][0]['address'].lstrip(),clos))
                print(b["routes"][0]["legs"][0]["distance"]["text"]+", "+b["routes"][0]["legs"][0]["duration"]["text"])
                print(a["routes"][0]["legs"][0]["distance"]["text"]+", "+a["routes"][0]["legs"][0]["duration"]["text"])
                
                ret = {
                    "walk_polyline":b["routes"][0]["overview_polyline"],
                    "walk_distance":b["routes"][0]["legs"][0]["distance"]["text"],
                    "walk_time":b["routes"][0]["legs"][0]["duration"]["text"],
                    "bike_polyline":a["routes"][0]["overview_polyline"],
                    "bike_distance":a["routes"][0]["legs"][0]["distance"]["text"],
                    "bike_time":a["routes"][0]["legs"][0]["duration"]["text"],
                    "bike_station":clos["name"]
                    }

                x["address"][0]["citibike"] = ret
                c.teachers.Collections.update({"id":x['id']},{"$set":{"address":x["address"]}})


            else:
                print("\t\tERROR: %s %s, %s"%(x['first'],x['last'],x['address'][0]['address'].lstrip()))



    
if __name__ == "__main__":
    updateTeachers()
#    print(str(closest(0,0,docks)))
