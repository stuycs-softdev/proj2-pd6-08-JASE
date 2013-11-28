

import urllib2
import json
from pymongo import MongoClient


def getCoords(a):
    url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false"%(a.replace(" ","+"))

    request = urllib2.Request(url, headers={'User-Agent':"Firefox Browser"})
    result = urllib2.urlopen(url)

    r = {}
    try:
        k = json.loads(result.read())["results"][0]

    

        r["borough"] = k["address_components"][3]["long_name"]
        r["neighborhood"] = k["address_components"][2]["long_name"]
        r["lat"] = k["geometry"]["location"]["lat"]
        r["long"] = k["geometry"]["location"]["lng"]
    except:
        return -1

    return r

#    return r#[k["lat"],k["lng"]]

#    return k


    

def updateTeachers():
    c = MongoClient()

    for x in c.teachers.Collections.find():
        if len(x["address"]) > 0:
            addr = []
#            for y in x["address"]:
            y = x["address"][0]
            if True:
                try:
                    k = getCoords(y['address'].lstrip())
                    for z in k.keys():
                        y[z] = k[z]
                        addr.append(y)
                    print("%s %s - %s - %s"%(x['first'],x['last'],y['address'],str(k)))
                except:
                    pass

            c.teachers.Collections.update({"id":x['id']},{"$set":{"address":addr}})



if __name__ == "__main__":
#    print(str(getCoords("505 E 79 St, 10075")))
    updateTeachers()



