import urllib
from bs4 import BeautifulSoup
from operator import itemgetter

def getRatings():
    
    url = "http://www.ratemyteachers.com/stuyvesant-high-school/13765-s"

    page = BeautifulSoup(urllib.urlopen(url))

    results = []

    for x in page.find("table").find_all("tr"):
        if len(x.find_all("td")) > 0:
            name = x.find_all("td")[0].find("span").get_text()
        
            print(name)
           

    return page


if __name__ == "__main__":
    getRatings()
