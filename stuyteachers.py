
import urllib
from bs4 import BeautifulSoup
from operator import itemgetter

def getTeachers():
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
                
#            r.append([n[0],n[1]])


    return r

if __name__ == "__main__":
    data = getTeachers()
    data = sorted(data, key=itemgetter("title"))
    for x in data:
        print("%s,%s\t%s"%(x['last'],x['first'],x['title']))
