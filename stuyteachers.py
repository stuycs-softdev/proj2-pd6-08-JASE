
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
    
    teachers = getTeachers()
    for x in range(0,len(teachers)):
        teachers[x]["id"] = x
        c.teachers.Collections.insert(teachers[x])


if __name__ == "__main__":
    teachersToDatabase()
#    data = getTeachers("gasdf")
#    for x in data:
#        print("%s,%s,%s"%(x['last'],x['first'],x['title']))
