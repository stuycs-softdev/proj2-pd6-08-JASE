
import urllib
from bs4 import BeautifulSoup

def getTeachers():
    url = "http://stuy.enschool.org/apps/staff/"
    result = BeautifulSoup(urllib.urlopen(url))

    r = []
    for x in result.find("table").find_all("tr"):
        name = x.find("td").find("a")
        if name:
            r.append(name.get_text())

    return r

if __name__ == "__main__":
    teachers = getTeachers()
    for x in teachers:
        print(x)
