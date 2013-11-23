
## ACCESS TEACHER LIST:
## getTeachers(SORT)
## available options:
## - first
## - last (DEFAULT if left blank)
## - title
##
## returns dictionary of sorted results


import urllib
from bs4 import BeautifulSoup
from operator import itemgetter

from pymongo import MongoClient


# our functions
import pFinder # gets addresses and phone numbers
import salary  # gets salary
import ratemt  # ratemyteachers.com

def getTeachers(s=None):
    url = "http://stuy.enschool.org/apps/staff/"
    result = BeautifulSoup(urllib.urlopen(url))

    r = []
    for x in result.find("table").find_all("tr"):
        name = x.find("td").find("a")
        if name:
            n = name.get_text().split(". ")[1].split(" ")

            r.append({
                "first":n[0],
                "last":n[1],
                "title":x.find_all("td")[1].get_text()
                })
                

    if r and s in r[0].keys():
        r = sorted(r, key=itemgetter(s))
    
    return r

def teachersToDatabase():
    c = MongoClient()
    c.teachers.Collections.remove()

    print("Adding in teachers to database...")
    
    teachers = getTeachers()
    for x in range(0,len(teachers)):
        t = teachers[x]
        t["id"] = x


        # add in teacher's salary
        gs = salary.getSalary(t["first"],t["last"])
        t["salary"] = int(gs[0])
        t["salary_year"] = int(gs[1])

        # array for multiple address results of teachers
        t["address"] = []
        addr = pFinder.pFind(t["first"],t["last"])

        for z in addr:
            # z["map"] = gmap()  --- placeholder for Google Maps function
            t["address"].append(z)

        
            

        c.teachers.Collections.insert(teachers[x])

#        if t["salary"] == -1:
#            print("[%d] Error  %s %s"%(x,t["first"],t["last"]))
#        else:
        pr = "[%d]\t{{ %s %s }}\t"%(x,t["first"],t["last"])
        if t["salary"] == -1:
            pr += "Error "
        else:
            pr += "$%d"%(t["salary"])
        if(len(t["address"]) > 0):
            pr += "\t%s\t%s"%(t["address"][0]["phoneNum"],t["address"][0]["address"])
        else:
            pr += "No address found"
        pr += "\n"
        print(pr)



    # compare ratemyteachers
    print("Searching up results from ratemyteachers.com:")
    
    res = ratemt.getRatings()
    
    for x in range(0,len(res)):
        res[x]["id"] = x
        c.ratemt.Collections.insert(res[x])
    



if __name__ == "__main__":
    c = MongoClient()
    c.ratemt.Collections.remove()
    print("Searching up results from ratemyteachers.com:")
    
    res = ratemt.getRatings()
    
    for x in range(0,len(res)):
        res[x]["overall"] = int(res[x]["overall"].replace("%",""))
        res[x]["id"] = x
        c.ratemt.Collections.insert(res[x])

#    teachersToDatabase()

