

import urllib2
import json
from pymongo import MongoClient

def getStuff(a):
    url = 'http://maps.googleapis.com/maps/api/directions/json?origin=%s&destination=Stuyvesant+High+School&sensor=false&mode=transit&arrival_time=47000'%(a.replace(" ","+"))

    result = urllib2.urlopen(url)


    try:
        k = json.loads(result.read())
        
        return k
    except:
        return None


def getTeachs():
    c = MongoClient()

    for x in c.teachers.Collections.find():
        if len(x["address"]) > 0:
            x["address"][0]["directions"] = getStuff(x["address"][0]["address"].lstrip())
           
            print("%s %s"%(x["first"],x["last"]))
 
            c.teachers.Collections.update({"id":x['id']},{"$set":{"address":x["address"]}})


if __name__ == "__main__":
    getTeachs()

