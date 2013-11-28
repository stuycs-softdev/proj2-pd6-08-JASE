
import time
import urllib2
import json
from pymongo import MongoClient

def getStuff(a):
    url = 'http://maps.googleapis.com/maps/api/directions/json?origin=%s&destination=Stuyvesant+High+School&sensor=false&mode=transit&arrival_time=47000'%(a.replace(" ","+"))

    result = urllib2.urlopen(url)


    try:
        k = json.loads(result.read())

        if k["status"] == "OVER_QUERY_LIMIT":
            time.sleep(2)
            return getStuff(a)
        
        return k
    except:
        return None


def getTeachs():
    c = MongoClient()

    for x in c.teachers.Collections.find():
        if len(x["address"]) > 0 and "lat" not in x["address"][0].keys():
            print("%s %s"%(x['first'],x['last']))

            addr = x["address"][0]["address"].lstrip()
            k = getStuff(addr)
            
            if len(k["routes"]) > 0:

#                while "error_message" in k:
#                    time.sleep(2)
#                    k = getStuff(x["address"][0]["address"].lstrip())
                
                    
                x["address"][0]["directions"] = k

                a = k["routes"][0]["legs"][0]["start_location"]
                
                x["address"][0]["lat"] = a["lat"]
                x["address"][0]["long"] = a["lng"]
           
                print("\t"+str(a["lat"])+","+str(a["lng"]))
                
                c.teachers.Collections.update({"id":x['id']},{"$set":{"address":x["address"]}})

if __name__ == "__main__":
    getTeachs()

